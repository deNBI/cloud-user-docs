import re
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


ACTIVE_CONTENT = re.compile(
    # href may only point inside the document (#id) or to an embedded raster image.
    r"<script|javascript:|<foreignobject|\son[a-z]+\s*=|href\s*=\s*[\"']?(?!#|data:image/)[^\"'\s>]",
    re.IGNORECASE,
)


def active_content(svg_text: str) -> list[str]:
    """Scripts, event handlers, embedded documents and external references in an SVG."""
    return [m.group(0) for m in ACTIVE_CONTENT.finditer(svg_text)]


def test_active_content_detects_unsafe_svg():
    assert active_content('<svg><path d="M0 0"/><use href="#a"/></svg>') == []
    assert active_content('<svg><image xlink:href="data:image/png;base64,iVBO"/></svg>') == []
    for bad in ('<svg onload="x()">', '<svg><script>x()</script>', '<svg><image href="a.png"/>',
                '<svg><a xlink:href="https://example.org">', '<svg><foreignObject>',
                '<svg><a href="javascript:x()">'):
        assert active_content(bad), bad


THEME_SVGS = [WIKI / "assets/images", WIKI / "overrides"]


def test_svgs_have_no_active_content():
    for svg in WIKI.glob("**/*.svg"):
        if "mathjax" in svg.parts:
            continue
        found = active_content(svg.read_text(errors="ignore"))
        if not any(svg.is_relative_to(d) for d in THEME_SVGS):
            # Diagrams in pages (draw.io exports) use foreignObject for their labels.
            found = [f for f in found if f.lower() != "<foreignobject"]
        assert found == [], svg


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
