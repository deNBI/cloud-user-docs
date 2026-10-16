#!/usr/bin/env python3
"""Check that wiki URLs used by other de.NBI resources still resolve.

Reads inbound_links.txt and verifies each page and anchor against a built
copy of the wiki (the output directory of `mkdocs build`).

Usage: check_inbound_links.py <site_dir> [inbound_links.txt]
"""

import re
import sys
from pathlib import Path


def parse_entries(list_file):
    entries = []
    for number, line in enumerate(list_file.read_text().splitlines(), start=1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        url, _, source = line.partition(" ")
        entries.append((number, url, source.strip()))
    return entries


def resolve_page(site_dir, path):
    # use_directory_urls: "page/" and "page" both serve page/index.html
    path = path.strip("/")
    candidates = [site_dir / path / "index.html"]
    if path.endswith(".html"):
        candidates.insert(0, site_dir / path)
    return next((c for c in candidates if c.is_file()), None)


def check(site_dir, list_file):
    errors = []
    for number, url, source in parse_entries(list_file):
        path, _, anchor = url.partition("#")
        page = resolve_page(site_dir, path)
        if page is None:
            errors.append(f"{list_file.name}:{number}: page not found: {url}  ({source})")
            continue
        if anchor:
            html = page.read_text(encoding="utf-8")
            if not re.search(r"""\bid=["']?%s["'\s>]""" % re.escape(anchor), html):
                errors.append(f"{list_file.name}:{number}: anchor not found: {url}  ({source})")
    return errors


def main():
    if len(sys.argv) not in (2, 3):
        sys.exit(__doc__)
    site_dir = Path(sys.argv[1])
    list_file = Path(sys.argv[2] if len(sys.argv) == 3 else "inbound_links.txt")
    if not (site_dir / "index.html").is_file():
        sys.exit(f"{site_dir} does not look like a built wiki (no index.html)")

    errors = check(site_dir, list_file)
    for error in errors:
        print(error)
    if errors:
        print(f"\n{len(errors)} inbound link(s) broken. Update the linking resource and "
              f"{list_file.name}, or restore the page/heading.")
        sys.exit(1)
    print(f"All inbound links in {list_file.name} resolve.")


if __name__ == "__main__":
    main()
