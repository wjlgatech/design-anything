#!/usr/bin/env python3
"""build_readme.py — compile data/*.yml into README sections.

Humans edit data/*.yml; README tables between BEGIN/END markers are generated.
`--check` fails (exit 1) if the committed README drifts from the generator
output — the drift gate `make check` runs in CI.
"""

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
README = ROOT / "README.md"

TIER = {"gold": "🥇", "silver": "🥈", "bronze": "🥉", "watch": "👀",
        "survivor": "🏛", "young": "🌱"}


def load(name):
    return yaml.safe_load((DATA / name).read_text())


def tools_section():
    entries = load("tools.yml")
    cats = []
    for e in entries:
        if e["category"] not in cats:
            cats.append(e["category"])
    out = []
    for cat in cats:
        out.append(f"\n### {cat}\n")
        out.append("| Tier | Tool | What it is |")
        out.append("|---|---|---|")
        for e in entries:
            if e["category"] == cat:
                out.append(f"| {TIER.get(e.get('tier'), '—')} | [{e['name']}]({e['url']}) | {e['blurb']} |")
    return "\n".join(out) + "\n"


def papers_section():
    out = ["", "| Tier | Work | Why it matters |", "|---|---|---|"]
    for e in load("papers.yml"):
        out.append(f"| {TIER.get(e.get('tier'), '—')} | [{e['name']}]({e['url']}) | {e['blurb']} |")
    return "\n".join(out) + "\n"


def community_section():
    out = ["", "| Who | Kind | Domain | Why they matter |", "|---|---|---|---|"]
    for e in load("community.yml"):
        out.append(f"| [{e['name']}]({e['url']}) | {e.get('kind', '—')} | "
                   f"{e.get('domain', '—')} | {e['blurb']} |")
    return "\n".join(out) + "\n"


def skills_section():
    out = ["", "| Skill | Status | What it does |", "|---|---|---|"]
    for e in load("registry.yml"):
        out.append(f"| [{e['name']}]({e['url']}) | {e.get('status', '—')} | {e['blurb']} |")
    return "\n".join(out) + "\n"


SECTIONS = {
    "tools": tools_section,
    "papers": papers_section,
    "community": community_section,
    "skills": skills_section,
}


def render(text):
    for key, fn in SECTIONS.items():
        begin, end = f"<!-- BEGIN:{key} -->", f"<!-- END:{key} -->"
        if begin not in text or end not in text:
            print(f"build_readme: README missing markers for '{key}'")
            sys.exit(1)
        head, rest = text.split(begin, 1)
        _, tail = rest.split(end, 1)
        text = head + begin + "\n" + fn() + end + tail
    return text


def main():
    current = README.read_text()
    generated = render(current)
    if "--check" in sys.argv:
        if generated != current:
            print("build_readme: DRIFT — README.md does not match data/*.yml; run `make readme`")
            sys.exit(1)
        print("build_readme: OK (no drift)")
        return
    README.write_text(generated)
    print("build_readme: README.md regenerated")


if __name__ == "__main__":
    main()
