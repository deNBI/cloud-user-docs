from pathlib import Path


def built_pages(site: Path) -> list[str]:
    return sorted(
        p.relative_to(site).as_posix() for p in site.rglob("*.html")
        if p.relative_to(site).parts[0] not in ("assets", "search")
    )


def test_page_urls_unchanged(site):
    expected = (Path(__file__).parent / "page_urls.txt").read_text().split()
    assert built_pages(site) == expected
