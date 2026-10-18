import re

import pytest
import yaml

from conftest import ROOT, page

PAGES = ["", "Tutorials/Ansible/", "404.html"]

COLUMNS = {
    "Use": [("Support", "https://cloud.denbi.de/support/"),
            ("SimpleVM wiki", "https://simplevm.denbi.de/wiki/"),
            ("Training material (de.KCD)", "https://datenkompetenz.cloud/training/")],
    "de.NBI Cloud": [("Website home", "https://cloud.denbi.de/"),
                     ("Apply for a project", "https://cloud.denbi.de/register/"),
                     ("Portal login", "https://cloud.denbi.de/portal/"),
                     ("Service status", "https://status.cloud.denbi.de/")],
    "Legal": [("Terms of use", "https://cloud.denbi.de/about/policies/"),
              ("Imprint", "https://cloud.denbi.de/about/imprint/"),
              ("Cookie settings", "#__consent")],
}


class _TagsAsData(yaml.SafeLoader):
    """Loads config.yml's !ENV, !relative and !!python tags as plain data."""


def _plain(loader, suffix, node):
    if isinstance(node, yaml.SequenceNode):
        return loader.construct_sequence(node)
    if isinstance(node, yaml.MappingNode):
        return loader.construct_mapping(node)
    return loader.construct_scalar(node)


_TagsAsData.add_multi_constructor("!", _plain)
_TagsAsData.add_multi_constructor("tag:yaml.org,2002:python/", _plain)


def footer(site, path):
    return page(site, path).select_one("footer.denbi-footer")


@pytest.mark.parametrize("path", PAGES)
def test_footer_columns(site, path):
    cols = {n.find("h2").get_text(strip=True): [(a.get_text(strip=True), a["href"]) for a in n.select("a")]
            for n in footer(site, path).select("nav.denbi-footer__col")}
    assert cols == COLUMNS


@pytest.mark.parametrize("path", PAGES)
def test_footer_brand(site, path):
    b = footer(site, path).select_one(".denbi-footer__brand")
    assert b.select_one("a")["href"] == "https://cloud.denbi.de/"
    assert 'Part of de.NBI (say "DEN-bee")' in b.get_text()
    assert b.select_one(".denbi-footer__logos") is None  # logos live in their own row


@pytest.mark.parametrize("path", PAGES)
def test_footer_logo_row(site, path):
    grid = footer(site, path).select_one(".md-grid")
    order = [c["class"][0] for c in grid.find_all(recursive=False)]
    assert order == ["denbi-footer__cols", "denbi-footer__partners", "denbi-footer__legal"]
    groups = {g.find("h2").get_text(strip=True): [i["alt"] for i in g.select("img:not(.denbi-logo--dark)")]
              for g in grid.select(".denbi-footer__partners .denbi-footer__logos")}
    assert list(groups) == ["Funded by", "In collaboration with"]
    assert len(groups["Funded by"]) == 2 and len(groups["In collaboration with"]) == 2
    assert all(groups["Funded by"] + groups["In collaboration with"])


@pytest.mark.parametrize("path", PAGES)
def test_eu_notice_once(site, path):
    f = footer(site, path)
    assert len(f.select('img.denbi-logo--light[src*="eu-nextgenerationeu-en"]')) == 1
    assert len(f.select('img.denbi-logo--dark[src*="eu-nextgenerationeu-en-neg"]')) == 1


def test_footer_logo_variants(site):
    f = footer(site, "")
    assert f.select_one('img.denbi-logo--dark[src*="elixir-negative-orange"]')
    panel = f.select(".denbi-logo-panel img")
    assert len(panel) == 1 and "bmftr-en" in panel[0]["src"]


def test_footer_legal_line(site):
    legal = footer(site, "portal/allocation/").select_one(".denbi-footer__legal")
    assert re.search(r"© \d{4} de\.NBI", legal.get_text(" ", strip=True))
    assert legal.find("a", string="Edit this page on GitHub")["href"] == \
        "https://github.com/deNBI/cloud-user-docs/edit/dev/wiki/portal/allocation.md"
    assert [(a.get_text(strip=True), a["href"]) for a in legal.select("ul a")] == \
        [("de.NBI", "https://www.denbi.de/"), ("GitHub", "https://github.com/deNBI")]


def test_old_footer_gone(site):
    soup = page(site, "")
    assert soup.select_one(".md-social") is None and soup.select_one(".md-footer-links") is None
    assert len(soup.find_all("footer")) == 1


def test_simplevm_link_matches_config():
    cfg = yaml.load((ROOT / "config.yml").read_text(), Loader=_TagsAsData)
    use = next(c for c in cfg["extra"]["footer_columns"] if c["heading"] == "Use")
    url = next(link["url"] for link in use["links"] if link["label"] == "SimpleVM wiki")
    assert url == cfg["extra"]["simplevm_wiki_link"][1]  # the !ENV default
