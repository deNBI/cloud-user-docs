# Wiki Header and Footer Aligned with the Website: Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the wiki's stock Material header and footer with the de.NBI Cloud website's quick access bar, menu row and footer, in light and dark mode.

**Architecture:** Theme overrides in `wiki/overrides/` replace Material's `header` block (quick access bar + menu row), empty the `tabs` block (the sections move into the menu row), and replace `footer.html`. All links and labels live in `config.yml` under `extra:`, and all styling lives in one new stylesheet, `wiki/assets/css/chrome.css`, built on the tokens in `denbi.css`. A pytest suite builds the site once with `config_local.yml` and checks the rendered HTML.

**Tech Stack:** MkDocs 1.6.1, mkdocs-material 9.7.7 (Jinja templates), pymdown-extensions 11.0.2, uv, pytest + beautifulsoup4 (new dev group).

**Spec:** `docs/superpowers/specs/2026-10-18-wiki-website-chrome-design.md`

## Global Constraints

- Pinned versions stay as in `pyproject.toml` (mkdocs-material 9.7.7, pymdown-extensions 11.0.2); do not fork the theme. Only override partials and blocks.
- Page URLs must not change. Only the `nav:` structure in `config.yml` changes; no Markdown file moves.
- Links to the website are absolute (`https://cloud.denbi.de/...`). Internal wiki links go through Material's `| url` filter so they work on nested pages and on `404.html`.
- Colours only through `--denbi-*` tokens from `wiki/assets/css/denbi.css`. Cyan (`--denbi-cyan`) is a fill or icon colour only, never text on white.
- Official funder and partner logos are never recoloured.
- No language switch, no previous/next footer links (`navigation.footer` stays off), no breadcrumb.
- Local preview: `uv run mkdocs serve -f config_local.yml`. Tests: `uv run pytest`.
- Work stays on the feature branch. Nothing is merged to `dev`, `staging` or `main` before the joint release with the website.

## Review Focus

1. **Anchor links under a taller sticky header.** The menu row is 72px instead of Material's 48px, so clicking a heading permalink or a `#fragment` link must still show the heading below the header, not hidden behind it. Pinned in Task 5 (CSS `scroll-padding-top`, verified in the browser).
2. **Phone width (360px).** There must be no horizontal scroll. The quick access bar shows icons only and the wiki link keeps an accessible name. The drawer button opens Material's drawer with all 7 sections, and Apply shortens to "Apply". Pinned in Task 4 (accessible-name test) and Task 5 (`test_menu_row_has_drawer_button` + browser check).
3. **Search and the palette toggle inside the custom header.** The `/` and `s` shortcuts, the results overlay, and the light/dark toggle (which persists across pages) must keep working. Pinned in Task 5 (`test_menu_row_keeps_search_and_palette` + browser check).
4. **The 404 page and deep pages.** On `404.html` and on three-level pages such as `Tutorials/Ansible/`, every header and footer link must resolve. Pinned in Task 4 and Task 6 (tests run on `404.html` and a deep page).
5. **Dark mode logos.** The de.NBI logo swaps to the light variant. BMFTR sits on a light panel, and EU and ELIXIR swap to their official negative versions. Pinned in Task 6 (`test_footer_logo_variants`) and Task 7 (browser check).

---

## File Structure

| File | Responsibility |
|---|---|
| `pyproject.toml`, `uv.lock` | add `[dependency-groups] dev = ["pytest", "beautifulsoup4"]` |
| `tests/conftest.py` | session fixture: build the site once and load pages as soup |
| `tests/page_urls.txt` | baseline list of built page paths (guards "URLs must not change") |
| `tests/test_navigation.py` | nav regrouping |
| `tests/test_assets.py` | logos and icons are present and safe |
| `tests/test_header.py` | quick access bar + menu row |
| `tests/test_footer.py` | footer |
| `config.yml` | `theme.features`, `theme.logo`, `nav`, `extra.*` chrome data, `extra_css` |
| `wiki/overrides/main.html` | wires the blocks: `header`, `tabs` (emptied), `footer` |
| `wiki/overrides/partials/quick-access.html` | row 1 |
| `wiki/overrides/partials/header.html` | row 2 (overrides Material's `partials/header.html`) |
| `wiki/overrides/partials/footer.html` | footer (overrides Material's `partials/footer.html`) |
| `wiki/overrides/.icons/symbols/*.svg` | Material Symbols icons, copied from the website |
| `wiki/assets/images/denbi-logo-color.svg`, `denbi-logo-light.svg` | de.NBI logo, light and dark variants |
| `wiki/assets/images/partners/*` + `SOURCE.txt` | funder and partner logos, with their sources |
| `wiki/assets/css/chrome.css` | all header and footer styles, light and dark |
| `README.md` | local preview and tests |

## `extra` keys (the shared interface)

Every template task reads these keys from `config.yml`. Task 4 adds the first
four, and Task 6 adds the footer keys.

```yaml
extra:
  website_url: https://cloud.denbi.de/
  apply: { label: "Apply for a project", short_label: "Apply", url: "https://cloud.denbi.de/register/" }
  quick_links:            # icon = file name in overrides/.icons/symbols/ without .svg
    - { label: "Portal login",  url: "https://cloud.denbi.de/portal/",              icon: login }
    - { label: "Wiki",          url: "",                                            icon: menu_book, current: true }  # "" = wiki home
    - { label: "Status",        url: "https://status.cloud.denbi.de/",              icon: dns }
    - { label: "Facility news", url: "https://cloud.denbi.de/news/facility-news/",  icon: campaign }
    - { label: "Support",       url: "https://cloud.denbi.de/support/",             icon: support_agent }
  footer_brand_text: 'Part of de.NBI (say "DEN-bee"), the German Network for Bioinformatics Infrastructure and ELIXIR Germany.'
  footer_logo_groups:     # light/dark: paths under wiki/; panel: light panel in dark mode
    - heading: "Funded by"
      logos:
        - { name: "Federal Ministry of Research, Technology and Space (BMFTR)", light: assets/images/partners/bmftr-en.png, panel: true }
        - { name: "Funded by the European Union – NextGenerationEU", light: assets/images/partners/eu-nextgenerationeu-en.png, dark: assets/images/partners/eu-nextgenerationeu-en-neg.png }
    - heading: "In collaboration with"
      logos:
        - { name: "ELIXIR", href: "https://elixir-europe.org/", light: assets/images/partners/elixir-standard.svg, dark: assets/images/partners/elixir-negative-orange.svg }
        - { name: "LS Login", href: "https://www.lifescience-ri.eu/life-science-login/", light: assets/images/partners/ls-login.png }
  footer_columns:
    - heading: "Use"
      links:
        - { label: "Support", url: "https://cloud.denbi.de/support/" }
        - { label: "SimpleVM wiki", url: "https://simplevm.denbi.de/wiki/" }   # same value as simplevm_wiki_link
        - { label: "Training material (de.KCD)", url: "https://datenkompetenz.cloud/training/" }
    - heading: "de.NBI Cloud"
      links:
        - { label: "Website home", url: "https://cloud.denbi.de/" }
        - { label: "Apply for a project", url: "https://cloud.denbi.de/register/" }
        - { label: "Portal login", url: "https://cloud.denbi.de/portal/" }
        - { label: "Service status", url: "https://status.cloud.denbi.de/" }
    - heading: "Legal"
      links:
        - { label: "Terms of use", url: "https://cloud.denbi.de/about/policies/" }
        - { label: "Imprint", url: "https://cloud.denbi.de/about/imprint/" }
        - { label: "Cookie settings", url: "#__consent" }
  footer_legal_links:
    - { label: "de.NBI", url: "https://www.denbi.de/" }
    - { label: "GitHub", url: "https://github.com/deNBI" }
```

The SimpleVM URL is a literal here because YAML can't reference the `!ENV`
value of `simplevm_wiki_link` from another key. Keep the literal; Task 6 has
a test that keeps the two values equal.

---

### Task 1: Test harness and URL baseline

**Files:**
- Modify: `pyproject.toml`, `uv.lock`
- Create: `tests/conftest.py`, `tests/page_urls.txt`, `tests/test_navigation.py`

**Interfaces:**
- Produces: the session fixture `site() -> pathlib.Path` (the build directory) and the helper `page(site: Path, path: str) -> bs4.BeautifulSoup`, where `path` is like `""`, `"portal/allocation/"` or `"404.html"`. Both live in `tests/conftest.py`; `page` is a plain function the tests import with `from conftest import page`.

- [ ] **Step 1: Add the dev group.** Run `uv add --dev pytest beautifulsoup4`, then check that `pyproject.toml` has a `[dependency-groups] dev` entry and that `uv.lock` changed.
- [ ] **Step 2: Write `tests/conftest.py`.** The `site` fixture (scope `session`) runs `mkdocs build -f config_local.yml -d <tmp>` through `subprocess.run([sys.executable, "-m", "mkdocs", ...], check=True, cwd=<repo root>)` and returns the directory. `page()` reads `<site>/<path>/index.html` (or `<site>/<path>` when `path` ends in `.html`) and parses it with `html.parser`.
- [ ] **Step 3: Write the baseline.** Build once and write every built `**/index.html` path plus `404.html`, relative to the site and sorted, one per line, to `tests/page_urls.txt`. Skip `assets/` and `search/`.
- [ ] **Step 4: Write the test.**

```python
def test_page_urls_unchanged(site):
    built = sorted(p.relative_to(site).as_posix() for p in site.rglob("*.html")
                   if not p.relative_to(site).parts[0] in ("assets", "search"))
    expected = (Path(__file__).parent / "page_urls.txt").read_text().split()
    assert built == expected
```

- [ ] **Step 5: Run it.** `uv run pytest tests/test_navigation.py -v`. Expected: PASS (this is the guard for later tasks).
- [ ] **Step 6: Commit.** `git add pyproject.toml uv.lock tests/ && git commit -m "test: build the wiki in tests and pin its page URLs"`

### Task 2: Regroup the navigation into 7 sections

**Files:**
- Modify: `config.yml` (`nav:`, `theme.features`)
- Test: `tests/test_navigation.py`

**Interfaces:**
- Produces: top-level `nav` titles, in order: `Getting started`, `Portal`, `SimpleVM`, `OpenStack`, `Tutorials`, `Sites`, `FAQ`, and the `navigation.tabs` feature turned on. Task 5 renders `nav.items` as the menu.

- [ ] **Step 1: Write the failing tests.**

```python
SECTIONS = ["Getting started", "Portal", "SimpleVM", "OpenStack", "Tutorials", "Sites", "FAQ"]

def test_top_level_sections(site):
    soup = page(site, "")
    top = soup.select("nav.md-nav--primary > ul.md-nav__list > li.md-nav__item")
    labels = [li.find(class_="md-nav__link").get_text(" ", strip=True) for li in top]
    assert labels == SECTIONS

def test_cloud_admin_is_under_sites(site):
    soup = page(site, "cloud_admin/project_management/")
    active = soup.select_one("nav.md-nav--primary > ul > li.md-nav__item--active")
    assert active.find(class_="md-nav__link").get_text(" ", strip=True) == "Sites"
    assert "For site administrators" in active.get_text()
```

- [ ] **Step 2: Run them.** `uv run pytest tests/test_navigation.py -v`. Expected: both FAIL (labels are the old 12).
- [ ] **Step 3: Rewrite `nav:` in `config.yml`.** Use the spec's table. `Getting started` lists `index.md` first, then Registration, Citation and publication, Security. `OpenStack` lists `quickstart.md` as "OpenStack Quickstart", then a `Concept` sub-group with the existing entries. `Sites` holds the eight compute centres, then a sub-group `For site administrators` with the five Cloud Admin pages. `FAQ: FAQ.md`. Keep every page title as it is today. Add `navigation.tabs` to `theme.features` (not `navigation.tabs.sticky`).
- [ ] **Step 4: Run the whole suite.** `uv run pytest -v`. Expected: all PASS, including `test_page_urls_unchanged`.
- [ ] **Step 5: Commit.** `git commit -am "feat(nav): group the wiki into seven sections"`

### Task 3: Logos and icons

**Files:**
- Create: `wiki/assets/images/denbi-logo-color.svg`, `wiki/assets/images/denbi-logo-light.svg`, `wiki/assets/images/partners/{bmftr-en.png,eu-nextgenerationeu-en.png,elixir-standard.svg,elixir-negative-orange.svg,ls-login.png,SOURCE.txt}`, `wiki/overrides/.icons/symbols/{login,menu_book,dns,campaign,support_agent}.svg`
- Test: `tests/test_assets.py`

**Interfaces:**
- Produces: the file paths above. Templates reference icons as `{% include ".icons/symbols/<name>.svg" %}` and images through `config.extra` paths.

- [ ] **Step 1: Write the failing tests.**

```python
WIKI = Path(__file__).parents[1] / "wiki"
LOGOS = ["denbi-logo-color.svg", "denbi-logo-light.svg"]
PARTNERS = ["bmftr-en.png", "eu-nextgenerationeu-en.png", "elixir-standard.svg",
            "elixir-negative-orange.svg", "ls-login.png", "SOURCE.txt"]
ICONS = ["login", "menu_book", "dns", "campaign", "support_agent"]

def test_files_exist():
    for f in LOGOS: assert (WIKI / "assets/images" / f).is_file()
    for f in PARTNERS: assert (WIKI / "assets/images/partners" / f).is_file()
    for i in ICONS: assert (WIKI / "overrides/.icons/symbols" / f"{i}.svg").is_file()

def test_svgs_have_no_active_content():
    for svg in WIKI.glob("**/*.svg"):
        if "mathjax" in svg.parts: continue
        text = svg.read_text(errors="ignore").lower()
        assert "<script" not in text and "javascript:" not in text, svg

def test_light_logo_has_no_dark_lettering():
    text = (WIKI / "assets/images/denbi-logo-light.svg").read_text().upper()
    for dark in ("#231F20", "#58595B", "#929497"):
        assert dark not in text
    for brand in ("#005AA9", "#00ADEE", "#EB008B"):
        assert brand in text

def test_partner_sources_documented():
    src = (WIKI / "assets/images/partners/SOURCE.txt").read_text()
    for f in PARTNERS[:-1]: assert f in src
```

- [ ] **Step 2: Run them.** `uv run pytest tests/test_assets.py -v`. Expected: FAIL (files missing).
- [ ] **Step 3: Copy the de.NBI logo and icons.**
  - Copy `../landing_page/landing_page/static/images/denbi-logo-color.svg` to `denbi-logo-color.svg`.
  - Create `denbi-logo-light.svg` from it with these exact replacements (case-insensitive): `#231F20` → `#E6EEF6`, `#58595B` → `#C3CFDB`, `#929497` → `#A7B6C7`.
  - Copy the five icons from `../landing_page/landing_page/static/cloud/icons/`, together with a copy of its `SOURCE.txt`.
  - Add `fill="currentColor"` to each icon's `<svg>` tag, and remove its `width` and `height` attributes.
- [ ] **Step 4: Get the partner logos.** Download into a scratch folder and check each before copying it in:
  - **BMFTR:** download `https://datenkompetenz.cloud/media/original_images/BMFTR_en_DTP_CMYK_gef_durch.jpg` and convert it to sRGB PNG without touching the artwork: `sips -s format png --matchTo "/System/Library/ColorSync/Profiles/sRGB Profile.icc" <in> --out bmftr-en.png`. Then scale it to 600px wide with `sips -Z 600`.
  - **EU:** get the official **English** horizontal "Funded by the European Union – NextGenerationEU" logo from the European Commission, and convert it to `eu-nextgenerationeu-en.png` (≤ 600px). If you can't find an official English source, stop and ask; do not use a third-party copy.
  - **ELIXIR:** copy `~/Downloads/ELIXIR_logo_standard(1).svg` → `elixir-standard.svg` and `~/Downloads/ELIXIR_logo_negative_orange(1).svg` → `elixir-negative-orange.svg`.
  - **LS Login:** download `https://www.lifescience-ri.eu/wp-content/uploads/2025/09/login-grey-wide.jpg.png` → `ls-login.png`.
  - **SOURCE.txt:** one line per file with its source URL (or "supplied by the maintainer, 2026-10-18" for ELIXIR) and the date.
- [ ] **Step 5: Run the tests.** `uv run pytest tests/test_assets.py -v`. Expected: PASS.
- [ ] **Step 6: Commit.** `git add wiki/assets/images wiki/overrides/.icons tests/test_assets.py && git commit -m "feat(theme): add the website logo, partner logos and icons"`

### Task 4: Quick access bar

**Files:**
- Modify: `config.yml` (`extra.website_url`, `extra.apply`, `extra.quick_links`; add `assets/css/chrome.css` to `extra_css` after `denbi.css`), `wiki/overrides/main.html`
- Create: `wiki/overrides/partials/quick-access.html`, `wiki/assets/css/chrome.css`
- Test: `tests/test_header.py`

**Interfaces:**
- Consumes: icons from Task 3; `extra` keys as listed above.
- Produces: `main.html`'s `{% block header %}`, which includes `partials/quick-access.html` and then `partials/header.html`. Task 5 fills `header.html`; until then Material's own header is used. Also produces the `chrome.css` sections `/* Quick access */`, `/* Menu row */`, `/* Footer */` and `/* Dark mode */`, which later tasks add to.

- [ ] **Step 1: Write the failing tests.** Run them for `""`, `"Tutorials/Ansible/"` and `"404.html"` with `@pytest.mark.parametrize("path", ...)`.

```python
QUICK = [("Portal login", "https://cloud.denbi.de/portal/"),
         ("Status", "https://status.cloud.denbi.de/"),
         ("Facility news", "https://cloud.denbi.de/news/facility-news/"),
         ("Support", "https://cloud.denbi.de/support/")]

def test_quick_access_bar(site, path):
    bar = page(site, path).select_one("div.denbi-quick")
    back = bar.select_one("a.denbi-quick__back")
    assert back["href"] == "https://cloud.denbi.de/"
    assert back.get_text(" ", strip=True) == "← de.NBI Cloud website"
    nav = bar.select_one("nav[aria-labelledby]")
    assert bar.select_one("#" + nav["aria-labelledby"]).get_text(strip=True) == "Quick access"
    links = [(a.select_one(".denbi-quick__text").get_text(strip=True), a["href"]) for a in nav.select("a")]
    assert [l for l in links if l[0] != "Wiki"] == QUICK
    wiki = nav.select_one('a[aria-current="true"]')
    assert wiki.select_one(".denbi-quick__text").get_text(strip=True) == "Wiki"
    assert wiki.find("svg") is not None
```

  Also add `test_quick_access_wiki_link_resolves`: on `"Tutorials/Ansible/"` the Wiki link's `href` resolves (`urllib.parse.urljoin("https://cloud.denbi.de/wiki/Tutorials/Ansible/", href)`) to `https://cloud.denbi.de/wiki/`. On `404.html`, check that it is `/wiki/` or `https://cloud.denbi.de/wiki/` (Material makes 404 links absolute from `site_url`).
- [ ] **Step 2: Run them.** `uv run pytest tests/test_header.py -v`. Expected: FAIL (`div.denbi-quick` missing).
- [ ] **Step 3: Implement `partials/quick-access.html`.** Use these classes:
  - `div.denbi-quick > div.md-grid`, containing:
    - `a.denbi-quick__back`: `<span aria-hidden="true">←</span> de.NBI Cloud website`
    - `span#denbi-quick-label.denbi-quick__label` "Quick access"
    - `nav[aria-labelledby=denbi-quick-label] > ul > li > a.denbi-quick__link`, each with the icon (`aria-hidden="true"`) and `span.denbi-quick__text`.
  - A link with an empty `url` points to `nav.homepage.url | url`. A link with `current: true` gets `aria-current="true"`.
  - In `main.html`: `{% block header %}{% include "partials/quick-access.html" %}{% include "partials/header.html" %}{% endblock %}`.
- [ ] **Step 4: Style it in `chrome.css` (`/* Quick access */`).**
  - Port `.quick` from `cloud.css` lines 157–170: background `--denbi-ink` (light mode `#042746`), white links, icon colour `--denbi-cyan`, label `#8fb3d6`, uppercase, `.06em` letter spacing, min-height 40px, font size 15px.
  - A 1px divider after the back link.
  - Below 900px, hide the label and visually hide `.denbi-quick__text`, using the website's clip technique so it keeps an accessible name, except on the back link.
  - The bar is not sticky.
- [ ] **Step 5: Run the tests.** `uv run pytest -v`. Expected: PASS.
- [ ] **Step 6: Check it in the browser.** `uv run mkdocs serve -f config_local.yml`, open `http://127.0.0.1:8000/`, and compare against the website's quick access bar at desktop width and at 360px. Expected: same height, colours and spacing; icons only at 360px; no horizontal scroll.
- [ ] **Step 7: Commit.** `git add -A config.yml wiki/overrides wiki/assets/css/chrome.css tests/test_header.py && git commit -m "feat(theme): add the website's quick access bar to the wiki"`

### Task 5: Menu row

**Files:**
- Create: `wiki/overrides/partials/header.html` (copy Material 9.7.7's `partials/header.html` as the starting point)
- Modify: `wiki/overrides/main.html` (`{% block tabs %}{% endblock %}`), `config.yml` (`theme.logo: assets/images/denbi-logo-color.svg`), `chrome.css` (`/* Menu row */`)
- Test: `tests/test_header.py`

**Interfaces:**
- Consumes: `extra.website_url`, `extra.apply`, the logos from Task 3, and the `nav.items` from Task 2.
- Produces: `header.md-header.denbi-header`, which Task 7 styles for dark mode.

- [ ] **Step 1: Write the failing tests.** Run them for `""`, `"portal/allocation/"`, `"Tutorials/Ansible/"` and `"404.html"`.

```python
def test_menu_row_logo_and_wordmark(site, path):
    h = page(site, path).select_one("header.md-header")
    logo = h.select_one("a.denbi-header__logo")
    assert logo["href"] == "https://cloud.denbi.de/"
    assert {i["src"].rsplit("/", 1)[1] for i in logo.find_all("img")} == {"denbi-logo-color.svg", "denbi-logo-light.svg"}
    assert all(i.get("alt") is not None for i in logo.find_all("img"))
    assert h.select_one("a.denbi-header__wordmark").get_text(strip=True) == "Wiki"

def test_menu_row_sections(site, path):
    items = page(site, path).select("header.md-header nav.denbi-sections a")
    assert [a.get_text(strip=True) for a in items] == SECTIONS   # import SECTIONS from test_navigation

def test_current_section_marked(site):
    cur = page(site, "portal/allocation/").select('nav.denbi-sections a[aria-current="true"]')
    assert [a.get_text(strip=True) for a in cur] == ["Portal"]

def test_apply_button(site, path):
    a = page(site, path).select_one("header.md-header a.denbi-header__apply")
    assert a["href"] == "https://cloud.denbi.de/register/"
    assert a.select_one(".denbi-header__apply-long").get_text(strip=True) == "Apply for a project"
    assert a.select_one(".denbi-header__apply-short").get_text(strip=True) == "Apply"

def test_menu_row_keeps_search_and_palette(site, path):
    h = page(site, path).select_one("header.md-header")
    assert h.select_one('label[for="__search"]') and h.select_one(".md-search")
    assert h.select_one("form[data-md-component=palette]")

def test_menu_row_has_drawer_button(site, path):
    assert page(site, path).select_one('header.md-header label[for="__drawer"]')

def test_no_material_tabs_or_repo_widget(site):
    soup = page(site, "")
    assert soup.select_one("nav.md-tabs") is None
    assert soup.select_one(".md-header__source") is None
```

  Section links must resolve to the section's first page. In `test_menu_row_sections`, also assert that on `"Tutorials/Ansible/"`, `urljoin("https://cloud.denbi.de/wiki/Tutorials/Ansible/", href)` for "Portal" equals `https://cloud.denbi.de/wiki/portal/allocation/`.
- [ ] **Step 2: Run them.** `uv run pytest tests/test_header.py -v`. Expected: the new tests FAIL.
- [ ] **Step 3: Implement `partials/header.html`.** Keep Material's skeleton: `header.md-header[data-md-component=header] > nav.md-header__inner.md-grid`, the `__drawer` label, `partials/palette.html` + `partials/javascripts/palette.html`, and the search label + `partials/search.html`. Remove the title/topic block and `partials/source.html`. In order:
  1. `a.denbi-header__logo` → `config.extra.website_url`, holding two `img`s (color with `alt="de.NBI Cloud"`, light with `alt=""`), both `src` via `| url`.
  2. `a.denbi-header__wordmark` "Wiki" → `nav.homepage.url | url`.
  3. `nav.denbi-sections[aria-label="Wiki sections"] > ul > li > a`, one per `nav.items`. The `href` is the first page of the item, found by walking `children` the same way Material's `partials/tabs-item.html` does. `aria-current="true"` when `nav_item.active`.
  4. The palette form, the search label and search.
  5. `a.denbi-header__apply.denbi-btn` with `span.denbi-header__apply-long` and `span.denbi-header__apply-short`.
  6. Add the class `denbi-header` to the `<header>`. In `main.html`, override `{% block tabs %}{% endblock %}`. Set `theme.logo` so the drawer shows the new logo.
- [ ] **Step 4: Style it (`/* Menu row */`).**
  - Port `.nav` from `cloud.css` lines 174–203 and `.btn`/`.btn-primary`/`.btn-sm` from lines 207–212:
    - white background, 1px `--denbi-line` bottom border
    - `--md-header-height` / `.md-header__inner` height `72px` (3.6rem)
    - logo 40px tall
    - wordmark in Raleway 700 with a 1px left divider
    - section links in Source Sans 3 600, `--denbi-ink`; hover and `[aria-current]` in `--denbi-blue`, with `box-shadow: inset 0 -2px 0` for the current one
  - Make the header `position: sticky; top: 0`. The quick access bar scrolls away above it, as on the website.
  - Fix the offsets that assume Material's 2.4rem header: `.md-sidebar { top: 3.6rem }` at ≥76.25em, plus `html { scroll-padding-top: 4.4rem }` so anchors land below the header (Review Focus 1). Check Material's compiled CSS for any other `top:2.4rem` rule, and override it only if it affects layout.
  - Show `nav.denbi-sections` only at ≥76.25em, Material's breakpoint for the lifted sidebar. Below that it's hidden, and the drawer button and drawer take over.
  - Show `.denbi-header__apply-short` instead of `-long` below 900px.
  - Show only the colour logo in this task. Task 7 swaps in the light one.
- [ ] **Step 5: Run the tests.** `uv run pytest -v`. Expected: PASS.
- [ ] **Step 6: Check it in the browser.** With `mkdocs serve`, check these points (Review Focus 1–3):
  - (a) At 1280px, the row matches the website's nav row.
  - (b) Clicking a heading's ¶ permalink on `portal/allocation/` shows the heading fully below the sticky header.
  - (c) `/` opens search, results appear, and Esc closes it.
  - (d) The palette toggle switches and survives navigation.
  - (e) At 360px, there's no horizontal scroll, the drawer opens and lists all 7 sections, and the button reads "Apply".
  - (f) The browser console shows no errors.
- [ ] **Step 7: Commit.** `git commit -am "feat(theme): website-style menu row with the wiki sections"` (add the new partial with `git add` first)

### Task 6: Footer

**Files:**
- Modify: `config.yml` (add `footer_brand_text`, `footer_logo_groups`, `footer_columns`, `footer_legal_links`; remove `extra.footer_links` and `extra.social`; change `edit_uri` from `blob/master/wiki/` to `edit/main/wiki/`), `wiki/overrides/main.html` (the `footer` block becomes `{% include "partials/footer.html" %}`), `chrome.css` (`/* Footer */`)
- Create: `wiki/overrides/partials/footer.html`
- Test: `tests/test_footer.py`

**Interfaces:**
- Consumes: the footer keys above, the logos from Task 3, and `page.edit_url` (from `repo_url` + `edit_uri`).
- Produces: `footer.md-footer.denbi-footer`, which Task 7 styles for dark mode.

- [ ] **Step 1: Write the failing tests.** Run them for `""`, `"Tutorials/Ansible/"` and `"404.html"`.

```python
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

def test_footer_columns(site, path):
    f = page(site, path).select_one("footer.denbi-footer")
    cols = {n.find("h2").get_text(strip=True): [(a.get_text(strip=True), a["href"]) for a in n.select("a")]
            for n in f.select("nav.denbi-footer__col")}
    assert cols == COLUMNS

def test_footer_brand(site, path):
    b = page(site, path).select_one("footer.denbi-footer .denbi-footer__brand")
    assert b.select_one("a")["href"] == "https://cloud.denbi.de/"
    assert 'Part of de.NBI (say "DEN-bee")' in b.get_text()
    assert b.select_one(".denbi-footer__logos") is None     # logos live in their own row

def test_footer_logo_row(site, path):
    grid = page(site, path).select_one("footer.denbi-footer > .md-grid")
    order = [c["class"][0] for c in grid.find_all(recursive=False)]
    assert order == ["denbi-footer__cols", "denbi-footer__partners", "denbi-footer__legal"]
    groups = {g.find("h2").get_text(strip=True): [i["alt"] for i in g.select("img:not(.denbi-logo--dark)")]
              for g in grid.select(".denbi-footer__partners .denbi-footer__logos")}
    assert list(groups) == ["Funded by", "In collaboration with"]
    assert len(groups["Funded by"]) == 2 and len(groups["In collaboration with"]) == 2

def test_eu_notice_once(site, path):
    f = page(site, path).select_one("footer.denbi-footer")
    assert len(f.select('img.denbi-logo--light[src*="eu-nextgenerationeu-en"]')) == 1
    assert len(f.select('img.denbi-logo--dark[src*="eu-nextgenerationeu-en-neg"]')) == 1

def test_footer_logo_variants(site):
    f = page(site, "").select_one("footer.denbi-footer")
    assert f.select_one('img.denbi-logo--dark[src*="elixir-negative-orange"]')
    panel = f.select(".denbi-logo-panel img")
    assert len(panel) == 1 and "bmftr-en" in panel[0]["src"]

def test_footer_legal_line(site):
    legal = page(site, "portal/allocation/").select_one("footer.denbi-footer .denbi-footer__legal")
    text = legal.get_text(" ", strip=True)
    assert re.search(r"© \d{4} de\.NBI", text)
    assert legal.find("a", string="Edit this page on GitHub")["href"] == \
           "https://github.com/deNBI/cloud-user-docs/edit/main/wiki/portal/allocation.md"
    assert [(a.get_text(strip=True), a["href"]) for a in legal.select("ul a")] == \
           [("de.NBI", "https://www.denbi.de/"), ("GitHub", "https://github.com/deNBI")]

def test_old_footer_gone(site):
    soup = page(site, "")
    assert soup.select_one(".md-social") is None and soup.select_one(".md-footer-links") is None
    assert len(soup.find_all("footer")) == 1

def test_simplevm_link_matches_config():
    cfg = yaml.load((ROOT / "config.yml").read_text(), Loader=_TagsAsData)
    use = next(c for c in cfg["extra"]["footer_columns"] if c["heading"] == "Use")
    url = next(l["url"] for l in use["links"] if l["label"] == "SimpleVM wiki")
    assert url == cfg["extra"]["simplevm_wiki_link"][1]   # the !ENV default
```

  `_TagsAsData` is a `yaml.SafeLoader` subclass (PyYAML ships with MkDocs). It registers `add_multi_constructor("!", ...)` and `add_multi_constructor("tag:yaml.org,2002:python/", ...)`, and both return the node's plain value (`construct_sequence` / `construct_scalar` / `construct_mapping`). It never constructs Python objects, so `config.yml`'s `!ENV`, `!relative` and `!!python/name` tags load as data.

- [ ] **Step 2: Run them.** `uv run pytest tests/test_footer.py -v`. Expected: FAIL.
- [ ] **Step 3: Implement `partials/footer.html`.**
  - `footer.md-footer.denbi-footer > div.md-grid`, containing:
    - `div.denbi-footer__cols` with `div.denbi-footer__brand` (logo link with both de.NBI logo variants, and the text) and one `nav.denbi-footer__col[aria-label=<heading>]` per column, each with `h2` + `ul > li > a`
    - then `div.denbi-footer__partners`: one compact row with one `div.denbi-footer__logos` per group (`h2` + logos), groups side by side
    - then `div.denbi-footer__legal`: `© {{ build_date_utc.year }} de.NBI`, the edit link if `page.edit_url`, and `ul` with the legal links
  - **Logos:** a logo with `dark` renders two `img`s, `.denbi-logo--light` and `.denbi-logo--dark`. A logo with `panel: true` is wrapped in `span.denbi-logo-panel`. A logo with `href` is wrapped in `a[rel=noopener]`. Every `img` has `alt=name` (the hidden dark twin gets `alt=""`), `height="48"`, and `src` via `| url`.
  - **Link targets:** links starting with `#` open in the same tab; external links don't force a new tab (same as the website).
- [ ] **Step 4: Style it (`/* Footer */`).**
  - Port `.site-footer` from `cloud.css` lines 657–672: `--denbi-bg-alt` background, top border, `48px 0 24px` padding, grid `1.6fr 1fr 1fr 1fr` with 32px gap, 2 columns ≤800px and 1 column ≤480px, `h2` in Raleway 15px `--denbi-muted`, `--denbi-ink` links with `--denbi-blue` underlined on hover.
  - Logo row `.denbi-footer__partners`: full width, top border `--denbi-line`, 24px top margin and padding, one flex row with wrap (32px gap between groups). Each group is a flex row with a small heading (`h2`, 13px, `--denbi-muted`) followed by its logos (16px gap, `img { height: 48px; width: auto }`), so on desktop all four logos sit on one line.
  - In light mode `.denbi-logo--dark` is `display: none`.
- [ ] **Step 5: Run the tests.** `uv run pytest -v`. Expected: PASS.
- [ ] **Step 6: Check it in the browser.** The footer matches the approved mockup (`.superpowers/brainstorm/*/content/footer-v2.html`), "Cookie settings" opens the consent dialog, and at 360px there's one column with no overflow.
- [ ] **Step 7: Commit.** `git add -A config.yml wiki/overrides wiki/assets/css/chrome.css tests/test_footer.py && git commit -m "feat(theme): website-style footer with funder and partner logos"`

### Task 7: Dark mode

**Files:**
- Modify: `wiki/assets/css/chrome.css` (`/* Dark mode */`)

**Interfaces:**
- Consumes: `.denbi-quick`, `.denbi-header`, `.denbi-footer`, `.denbi-footer__partners`, `.denbi-logo--light/--dark`, `.denbi-logo-panel`, and the `[data-md-color-scheme="slate"]` tokens in `denbi.css`.

- [ ] **Step 1: Write the CSS (no unit test; the markup is already pinned).** Everything goes under `[data-md-color-scheme="slate"]`:
  - quick access bar background `#06121e`, divider `--denbi-line`
  - menu row background `--denbi-bg`, bottom border `--denbi-line`, links `--denbi-ink`, hover and current `--denbi-blue`, search field on `--denbi-bg-alt`
  - Apply stays `#005aa9` with white text (literal values, because the token turns light blue in slate)
  - footer background `--denbi-bg-alt`, `h2` `--denbi-muted`
  - swap `.denbi-logo--light`/`--dark` and the two de.NBI header and footer logos
  - `.denbi-logo-panel { background: #fff; border-radius: var(--radius, 8px); padding: 4px 6px; display: inline-flex }`; in light mode the panel has no background or padding
- [ ] **Step 2: Check contrast.** Cyan icons (`#00adee`) on `#06121e` and white text on `#06121e` must reach at least 3:1 for icons and 4.5:1 for text. If they don't, pick a navy that does and note the value in the commit message.
- [ ] **Step 3: Check it in the browser.** In dark mode, compare to the approved mockup (option B in `.superpowers/brainstorm/*/content/dark-mode.html`). The light de.NBI logo shows in the header and footer, BMFTR and EU sit on white panels, ELIXIR shows white lettering, and LS Login is unchanged. Switch back to light mode: nothing from dark mode is left over.
- [ ] **Step 4: Run the suite.** `uv run pytest -v`. Expected: PASS.
- [ ] **Step 5: Commit.** `git commit -am "feat(theme): dark mode for the wiki header and footer"`

### Task 8: Docs and final verification

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Update the README.** Next to the existing uv preview instructions, add `uv run pytest` to run the checks, and one sentence that header and footer links live in `config.yml` under `extra:` and must be updated by hand when the website's Wagtail navigation changes.
- [ ] **Step 2: Run the full suite.** `uv run pytest -v`. Expected: all PASS.
- [ ] **Step 3: Run the link check as CI does.** `ENABLED_HTMLPROOFER=True uv run mkdocs build -f config_local.yml -d /tmp/wiki-site`. Expected: finishes without "htmlproofer" errors. Network-dependent; on failure, check whether the failing URL also fails on `main` before changing anything.
- [ ] **Step 4: Walk through it end to end in the browser.** Repeat the checks from Tasks 4–7 on `/`, `portal/allocation/`, `Tutorials/Ansible/`, `Compute_Center/Berlin/` and a missing URL (404), in light and dark mode, at 1280px and 360px.
- [ ] **Step 5: Commit.** `git commit -am "docs: explain the wiki header and footer configuration"`
