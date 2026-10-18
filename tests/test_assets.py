from pathlib import Path

WIKI = Path(__file__).resolve().parents[1] / "wiki"
LOGOS = ["denbi-logo-color.svg", "denbi-logo-light.svg"]
PARTNERS = ["bmftr-en.png", "eu-nextgenerationeu-en.png", "eu-nextgenerationeu-en-neg.png", "elixir-standard.svg",
            "elixir-negative-orange.svg", "ls-login.png", "SOURCE.txt"]
ICONS = ["login", "menu_book", "dns", "campaign", "support_agent"]


def test_files_exist():
    for f in LOGOS:
        assert (WIKI / "assets/images" / f).is_file(), f
    for f in PARTNERS:
        assert (WIKI / "assets/images/partners" / f).is_file(), f
    for i in ICONS:
        assert (WIKI / "overrides/.icons/symbols" / f"{i}.svg").is_file(), i


def test_svgs_have_no_active_content():
    for svg in WIKI.glob("**/*.svg"):
        if "mathjax" in svg.parts:
            continue
        text = svg.read_text(errors="ignore").lower()
        assert "<script" not in text and "javascript:" not in text, svg


def test_light_logo_has_no_dark_lettering():
    text = (WIKI / "assets/images/denbi-logo-light.svg").read_text().upper()
    for dark in ("#231F20", "#58595B", "#929497"):
        assert dark not in text
    for brand in ("#005AA9", "#00ADEE", "#EB008B"):
        assert brand in text


def test_icons_follow_text_colour():
    for i in ICONS:
        text = (WIKI / "overrides/.icons/symbols" / f"{i}.svg").read_text()
        assert 'fill="currentColor"' in text and "width=" not in text, i


def test_partner_sources_documented():
    src = (WIKI / "assets/images/partners/SOURCE.txt").read_text()
    for f in PARTNERS[:-1]:
        assert f in src, f
