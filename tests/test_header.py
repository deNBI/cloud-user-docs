from urllib.parse import urljoin

import pytest

from conftest import page
from test_navigation import SECTIONS

SITE_URL = "https://cloud.denbi.de/wiki/"
PAGES = ["", "Tutorials/Ansible/", "404.html"]

QUICK = [("Portal login", "https://cloud.denbi.de/portal/"),
         ("Status", "https://status.cloud.denbi.de/"),
         ("Facility news", "https://cloud.denbi.de/news/facility-news/"),
         ("Support", "https://cloud.denbi.de/support/")]


def resolve(path: str, href: str) -> str:
    base = SITE_URL if path.endswith(".html") else SITE_URL + path
    return urljoin(base, href)


@pytest.mark.parametrize("path", PAGES)
def test_quick_access_bar(site, path):
    bar = page(site, path).select_one("div.denbi-quick")
    back = bar.select_one("a.denbi-quick__back")
    assert back["href"] == "https://cloud.denbi.de/"
    assert back.get_text(" ", strip=True) == "← de.NBI Cloud website"
    nav = bar.select_one("nav[aria-labelledby]")
    assert bar.select_one("#" + nav["aria-labelledby"]).get_text(strip=True) == "Quick access"
    links = [(a.select_one(".denbi-quick__text").get_text(strip=True), a["href"])
             for a in nav.select("a")]
    assert [link for link in links if link[0] != "Wiki"] == QUICK
    wiki = nav.select_one('a[aria-current="true"]')
    assert wiki.select_one(".denbi-quick__text").get_text(strip=True) == "Wiki"
    assert all(a.find("svg") is not None for a in nav.select("a"))


# Same badge as the website's quick access bar (landing_page STATUS_BADGE_URL).
STATUS_BADGE = ("https://status.cloud.denbi.de/api/status-page/default/badge"
                "?style=flat-square&upColor=2e7d32&downColor=c62828"
                "&partialColor=b45309&maintenanceColor=5f6368")


@pytest.mark.parametrize("path", PAGES)
def test_status_link_shows_the_live_badge(site, path):
    nav = page(site, path).select_one("div.denbi-quick nav")
    badges = nav.select("img.denbi-quick__badge")
    assert len(badges) == 1
    badge = badges[0]
    status = badge.find_parent("a")
    assert status["href"] == "https://status.cloud.denbi.de/"
    assert badge["src"] == STATUS_BADGE
    assert badge["alt"] == "" and badge["height"] == "20"


@pytest.mark.parametrize("path", PAGES)
def test_quick_access_wiki_link_resolves(site, path):
    wiki = page(site, path).select_one('div.denbi-quick a[aria-current="true"]')
    assert resolve(path, wiki["href"]) == SITE_URL


MENU_PAGES = ["", "portal/allocation/", "Tutorials/Ansible/", "404.html"]


def header(site, path):
    return page(site, path).select_one("header.md-header")


@pytest.mark.parametrize("path", MENU_PAGES)
def test_menu_row_logo_and_wordmark(site, path):
    h = header(site, path)
    logo = h.select_one("a.denbi-header__logo")
    assert logo["href"] == "https://cloud.denbi.de/"
    imgs = logo.find_all("img")
    assert {i["src"].rsplit("/", 1)[1] for i in imgs} == {"denbi-logo-color.svg", "denbi-logo-light.svg"}
    assert all(i.get("alt") is not None for i in imgs)
    assert [i["alt"] for i in imgs if i["alt"]] == ["de.NBI Cloud"]
    wordmark = h.select_one("a.denbi-header__wordmark")
    assert wordmark.get_text(strip=True) == "Wiki"
    assert resolve(path, wordmark["href"]) == SITE_URL


@pytest.mark.parametrize("path", MENU_PAGES)
def test_menu_row_sections(site, path):
    items = header(site, path).select("nav.denbi-sections a")
    assert [a.get_text(strip=True) for a in items] == SECTIONS
    portal = next(a for a in items if a.get_text(strip=True) == "Portal")
    assert resolve(path, portal["href"]) == SITE_URL + "portal/allocation/"


def test_current_section_marked(site):
    cur = header(site, "portal/allocation/").select('nav.denbi-sections a[aria-current="true"]')
    assert [a.get_text(strip=True) for a in cur] == ["Portal"]


@pytest.mark.parametrize("path", MENU_PAGES)
def test_apply_button(site, path):
    a = header(site, path).select_one("a.denbi-header__apply")
    assert a["href"] == "https://cloud.denbi.de/register/"
    assert a.select_one(".denbi-header__apply-long").get_text(strip=True) == "Apply for a project"
    assert a.select_one(".denbi-header__apply-short").get_text(strip=True) == "Apply"


@pytest.mark.parametrize("path", MENU_PAGES)
def test_menu_row_keeps_search_and_palette(site, path):
    h = header(site, path)
    assert h.select_one('label[for="__search"]') and h.select_one(".md-search")
    assert h.select_one("form[data-md-component=palette]")


@pytest.mark.parametrize("path", MENU_PAGES)
def test_menu_row_has_drawer_button(site, path):
    assert header(site, path).select_one('label[for="__drawer"]')


def test_no_material_tabs_or_repo_widget(site):
    soup = page(site, "")
    assert soup.select_one("nav.md-tabs") is None
    assert soup.select_one(".md-header__source") is None
