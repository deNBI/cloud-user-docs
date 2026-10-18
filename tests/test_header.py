from urllib.parse import urljoin

import pytest

from conftest import page

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


@pytest.mark.parametrize("path", PAGES)
def test_quick_access_wiki_link_resolves(site, path):
    wiki = page(site, path).select_one('div.denbi-quick a[aria-current="true"]')
    assert resolve(path, wiki["href"]) == SITE_URL
