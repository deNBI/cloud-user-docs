from conftest import page


def test_home_invites_contributions(site):
    soup = page(site, "")
    heading = soup.find("h2", id="improve-this-wiki")
    assert heading is not None
    section = heading.find_next_sibling("div", class_="grid")
    cards = [li.find("strong").get_text(strip=True) for li in section.select(":scope > ul > li")]
    assert cards == ["Fix or improve a page", "Report a problem", "Add a page or tutorial"]
    hrefs = [a["href"] for a in section.select("a")]
    assert "https://github.com/deNBI/cloud-user-docs/issues/new" in hrefs
    assert "https://github.com/deNBI/cloud-user-docs#readme" in hrefs
    assert "dev" in section.get_text()
