#!/usr/bin/env python3
"""validate.py — schema gate for data/*.yml. Every entry needs name, url, blurb.

Exit 0 = valid, 1 = violations (gates CI).
"""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

REQUIRED = {"name", "url", "blurb"}
LIST_FILES = ["tools.yml", "papers.yml", "community.yml", "registry.yml"]


def check_entry(fname: str, i: int, e: dict) -> list[str]:
    """Schema rules for one curated entry."""
    errors = []
    label = f"{fname}[{i}] ({e.get('name', '?')})"
    missing = REQUIRED - set(e)
    if missing:
        errors.append(f"{label}: missing {sorted(missing)}")
    url = e.get("url", "")
    if url and not url.startswith("http"):
        errors.append(f"{label}: url must be http(s)")
    if len(e.get("blurb", "")) > 220:
        errors.append(f"{label}: blurb over 220 chars — one non-hypey sentence")
    return errors


def check_list_file(fname: str) -> list[str]:
    """A curated file must be a non-empty list of valid entries."""
    path = DATA / fname
    if not path.exists():
        return [f"{fname}: missing"]
    entries = yaml.safe_load(path.read_text())
    if not isinstance(entries, list) or not entries:
        return [f"{fname}: must be a non-empty list"]
    return [err for i, e in enumerate(entries) for err in check_entry(fname, i, e)]


def check_meta() -> list[str]:
    """meta.yml carries the branding keys the generators depend on."""
    meta = yaml.safe_load((DATA / "meta.yml").read_text())
    return [f"meta.yml: missing '{key}'"
            for key in ("title", "tagline", "why_different", "domains")
            if key not in meta]


def check_news() -> list[str]:
    """news.yml: dated entries, required keys, newest first."""
    news = yaml.safe_load((DATA / "news.yml").read_text())
    if not isinstance(news, list) or not news:
        return ["news.yml: must be a non-empty list"]
    errors = [f"news.yml[{i}]: missing '{key}'"
              for i, e in enumerate(news)
              for key in ("date", "title", "note") if key not in e]
    dates = [str(e.get("date", "")) for e in news]
    if dates != sorted(dates, reverse=True):
        errors.append("news.yml: entries must be newest first")
    return errors


def main() -> None:
    errors: list[str] = []
    for fname in LIST_FILES:
        errors.extend(check_list_file(fname))
    errors.extend(check_meta())
    errors.extend(check_news())

    if errors:
        print(f"validate: {len(errors)} violation(s)")
        for e in errors:
            print(f"  FAIL {e}")
        sys.exit(1)
    total = sum(len(yaml.safe_load((DATA / f).read_text())) for f in LIST_FILES)
    print(f"validate: OK ({total} entries across {len(LIST_FILES)} files)")


if __name__ == "__main__":
    main()
