from pathlib import Path

from conftest import page


def built_pages(site: Path) -> list[str]:
    return sorted(
        p.relative_to(site).as_posix() for p in site.rglob("*.html")
        if p.relative_to(site).parts[0] not in ("assets", "search")
    )


def test_page_urls_unchanged(site):
    expected = (Path(__file__).parent / "page_urls.txt").read_text().split()
    assert built_pages(site) == expected


SECTIONS = ["Getting started", "Portal", "SimpleVM", "OpenStack", "Tutorials", "Sites", "FAQ"]


def label(li) -> str:
    return li.find(class_="md-nav__link").get_text(" ", strip=True)


def test_top_level_sections(site):
    top = page(site, "").select("nav.md-nav--primary > ul.md-nav__list > li.md-nav__item")
    assert [label(li) for li in top] == SECTIONS


def test_cloud_admin_is_under_sites(site):
    soup = page(site, "cloud_admin/project_management/")
    active = soup.select_one("nav.md-nav--primary > ul > li.md-nav__item--active")
    assert label(active) == "Sites"
    assert "For site administrators" in active.get_text()


def test_theme_templates_not_published(site):
    assert not (site / "overrides").exists()
