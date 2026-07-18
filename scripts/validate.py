#!/usr/bin/env python3
"""validate.py — schema gate for data/*.yml. Every entry needs name, url, blurb.

Exit 0 = valid, 1 = violations (gates CI).
"""

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

REQUIRED = {"name", "url", "blurb"}
LIST_FILES = ["tools.yml", "papers.yml", "community.yml", "registry.yml"]


def main():
    errors = []
    for fname in LIST_FILES:
        path = DATA / fname
        if not path.exists():
            errors.append(f"{fname}: missing")
            continue
        entries = yaml.safe_load(path.read_text())
        if not isinstance(entries, list) or not entries:
            errors.append(f"{fname}: must be a non-empty list")
            continue
        for i, e in enumerate(entries):
            missing = REQUIRED - set(e)
            if missing:
                errors.append(f"{fname}[{i}] ({e.get('name', '?')}): missing {sorted(missing)}")
            url = e.get("url", "")
            if url and not url.startswith("http"):
                errors.append(f"{fname}[{i}] ({e.get('name', '?')}): url must be http(s)")
            blurb = e.get("blurb", "")
            if blurb and len(blurb) > 220:
                errors.append(f"{fname}[{i}] ({e.get('name', '?')}): blurb over 220 chars — one non-hypey sentence")

    meta = yaml.safe_load((DATA / "meta.yml").read_text())
    for key in ("title", "tagline", "why_different", "domains"):
        if key not in meta:
            errors.append(f"meta.yml: missing '{key}'")

    news = yaml.safe_load((DATA / "news.yml").read_text())
    if not isinstance(news, list) or not news:
        errors.append("news.yml: must be a non-empty list")
    else:
        for i, e in enumerate(news):
            for key in ("date", "title", "note"):
                if key not in e:
                    errors.append(f"news.yml[{i}]: missing '{key}'")
        dates = [str(e.get("date", "")) for e in news]
        if dates != sorted(dates, reverse=True):
            errors.append("news.yml: entries must be newest first")

    if errors:
        print(f"validate: {len(errors)} violation(s)")
        for e in errors:
            print(f"  FAIL {e}")
        sys.exit(1)
    total = sum(len(yaml.safe_load((DATA / f).read_text())) for f in LIST_FILES)
    print(f"validate: OK ({total} entries across {len(LIST_FILES)} files)")


if __name__ == "__main__":
    main()
