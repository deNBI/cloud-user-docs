from conftest import page

# The workplace sections of the security page, with the anchors other pages may link to.
SECTIONS = {
    "locking-your-office-door-a-simple-yet-effective-security-measure": "Lock your door",
    "locking-your-screen-protecting-sensitive-information-from-unintended-eyes": "Lock your screen",
    "the-hidden-dangers-of-found-usb-drives": "Leave found USB drives alone",
    "the-risk-of-unsecured-wi-fi-networks": "Avoid unsecured Wi-Fi",
    "the-dangers-of-improper-document-disposal": "Dispose of documents securely",
    "general-measures-and-awareness": "Stay aware",
}


def content(site):
    return page(site, "security/").select_one(".md-content")


def test_security_page_has_no_illustrations(site):
    assert content(site).select('img[src*="img/security"]') == []


def test_at_a_glance_links_every_section(site):
    heading = content(site).find(id="at-a-glance")
    cards = heading.find_next_sibling("div", class_="grid").select(":scope > ul > li")
    assert [(li.a["href"].lstrip("#"), li.a.get_text(strip=True)) for li in cards] == list(SECTIONS.items())
    for li in cards:
        assert li.select_one(".twemoji.denbi-tile svg"), li.a.get_text()
        assert li.p.get_text(strip=True), li.a.get_text()  # one-line rule under the title


def test_section_headings_keep_their_ids_and_get_an_icon(site):
    for anchor in SECTIONS:
        heading = content(site).find(id=anchor)
        assert heading is not None and heading.name == "h3", anchor
        assert heading.select_one(".twemoji.denbi-tile svg"), anchor


def test_table_of_contents_shows_no_icons(site):
    toc = page(site, "security/").select_one("nav.md-nav--secondary")
    assert toc.find("svg") is None
