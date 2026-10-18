from pathlib import Path
from xml.etree import ElementTree

from conftest import page

SITE_URL = "https://cloud.denbi.de/wiki/"


def built_pages(site: Path) -> list[str]:
    """Pages as MkDocs publishes them, from its sitemap, plus 404.html.

    Listing the files on disk would depend on the file system: on macOS, which
    ignores case, cloud_admin/elixir_OIDC/ lands in the Elixir_OIDC/ image folder.
    """
    sitemap = ElementTree.parse(site / "sitemap.xml").getroot()
    locs = [loc.text for loc in sitemap.iter("{http://www.sitemaps.org/schemas/sitemap/0.9}loc")]
    pages = [loc.removeprefix(SITE_URL) + "index.html" for loc in locs]
    # assets/ holds MathJax's own CONTRIBUTING page, not a wiki page.
    return sorted([p for p in pages if not p.startswith("assets/")] + ["404.html"])


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
