# Wiki header and footer aligned with the de.NBI Cloud website

Date: 2026-10-18
Branch: `feat/website-styles` (on top of `feat/persona-home-page` and `feat/uv-local-preview`)

## Intent

Readers move between the de.NBI Cloud website (Wagtail, `deNBI/landing_page`,
redesign on branch `feat/cloud-redesign`) and this wiki (MkDocs Material). Today
the wiki looks like a separate site: a different logo, Material's stock header,
and a footer made of three centred links. Going from the website to the wiki
should not feel like leaving the website. Both sites should feel like one,
with obvious ways back and forth.

The colours and fonts already match (commit "feat(theme): match the wiki's look
to the redesigned de.NBI Cloud website": `wiki/assets/css/denbi.css` uses the
website's colour values, and the font files are byte-identical). This design
covers the header (quick access bar and menu row), the footer, and how both
look in dark mode.

## Goals

- The wiki header uses the website's quick access bar, logo and menu-row style.
- There is a clear, always-visible link back to the website.
- The wiki footer uses the website's footer style, trimmed to what wiki readers need.
- Light and dark mode both look deliberate.

## Non-goals

- Automatic syncing with the Wagtail content. Links are copied into
  `config.yml` by hand; the maintainer accepted this.
- Carrying over everything from the website. Only what makes sense in the
  wiki is included (see below). The website's main menu (Services, Training,
  Research, …) is **not** shown in the wiki.
- A language switch. The wiki is English-only.
- Changing page content beyond the navigation regrouping.

## Anti-goals

- The wiki must not look like a second, competing homepage. The way back to
  cloud.denbi.de must never be hidden.
- No loss of existing wiki functions: search, the light/dark toggle, cookie
  consent (Matomo), the "last updated" date, and the instant navigation and
  permalinks of Material.

## Reference: the website (landing_page, `feat/cloud-redesign`)

- Templates: `home/templates/cloud/base.html`, `partials/quick_access.html`,
  `partials/nav.html`, `partials/footer.html`.
- Styles: `landing_page/static/cloud/css/cloud.css` (tokens at the top; quick
  access `.quick` from line ~157, menu row `.nav` from ~174, buttons `.btn`
  from ~207, footer `.site-footer` from ~657).
- Default content: `home/seed_content.py` (`SITE_CHROME`). The live values are
  edited in Wagtail, but they start from these values.
- Logo: `landing_page/static/images/denbi-logo-color.svg`.
- Icons: Material Symbols Outlined as inline SVG
  (`landing_page/static/cloud/icons/`, source in `SOURCE.txt`).

## Decided design

### Header (two rows)

**Row 1: quick access bar.** Copy of the website's `.quick` bar: navy
background (`--denbi-ink` / `#042746`), small type, cyan icons.

1. First item, separated by a thin divider: **"← de.NBI Cloud website"** →
   `https://cloud.denbi.de/`.
2. Label "QUICK ACCESS" (hidden on small screens, as on the website).
3. Links, with the same icons as the website:
   Portal login (`login`) → `https://cloud.denbi.de/portal/`,
   **Wiki** (`menu_book`) → wiki home, marked as the current page,
   Status (`dns`) → `https://status.cloud.denbi.de/`,
   Facility news (`campaign`) → `https://cloud.denbi.de/news/facility-news/`,
   Support (`support_agent`) → `https://cloud.denbi.de/support/`.

   On small screens the link labels become visually hidden and only the icons
   show, as on the website.

**Row 2: menu row.** Styled like the website's `.nav` row: white background,
1px bottom line, 72px tall on desktop.

- The website's colour logo (`denbi-logo-color.svg`), linking to
  `https://cloud.denbi.de/`. It replaces `wiki/img/denbi.svg` in the header.
- Right of the logo, after a thin vertical divider: the wordmark **"Wiki"**
  in Raleway, linking to the wiki home page.
- The wiki's top-level sections as menu items (see "Navigation regrouping"),
  styled like the website's menu links: navy, semibold, blue on hover. The
  current section is blue with a 2px blue underline. Use Material's
  `navigation.tabs`, moved into this row and restyled; no breadcrumb.
- On the right: search, the light/dark toggle, then the button
  **"Apply for a project"** (website `.btn .btn-primary .btn-sm` style) →
  `https://cloud.denbi.de/register/`. On narrow screens the label may shorten
  to "Apply".
- The left sidebar shows only the pages inside the current section, which is
  standard `navigation.tabs` behaviour.

### Navigation regrouping

The 12 current top-level entries become 7 sections. The maintainer accepted
this grouping "for now":

| Section | Contains (current `nav` entries) |
|---|---|
| Getting started | Home (`index.md`), Registration, Citation and publication, Security |
| Portal | all of Portal |
| SimpleVM | Simple VM |
| OpenStack | OpenStack Quickstart, Concept (Basics, Components, Flavors, Images, Image Builder, Network, Object Storage Giessen, Volumes) |
| Tutorials | all of Tutorials |
| Sites | Compute Center Specific (all sites), Cloud Admin (as a sub-group "For site administrators") |
| FAQ | FAQ |

Page URLs must not change. Only the `nav:` structure in `config.yml` changes;
no files move. Inbound links from other de.NBI resources depend on these URLs
(see the `inbound-link-check` work).

### Footer

Website `.site-footer` style: light grey-blue background (`--denbi-bg-alt`),
top border, a grid of one brand column (wider) and three link columns, then a
legal line.

- **Brand column:** the colour logo → `https://cloud.denbi.de/` and the text
  'Part of de.NBI (say "DEN-bee"), the German Network for Bioinformatics
  Infrastructure and ELIXIR Germany.'
- **Logo row** (maintainer's request, to keep the footer compact): one row
  spanning the full width, below the link columns and above the legal line,
  with two labelled groups side by side (see "Logos"):
  1. **Funded by** (maintainer's decision): BMFTR and the official EU
     NextGenerationEU logo. The EU logo *is* the EU funding notice, which the
     de.KCD training link requires. It appears exactly once in the footer;
     there is no separate flag-plus-text notice like the website's
     `eu_notice.html`.
  2. **In collaboration with** (maintainer's decision: ELIXIR and LS AAI must
     be in the footer): ELIXIR and LS Login (LS AAI). Splitting them into a
     second, labelled group so they don't read as funders is my call.
- **Use:** Support → `https://cloud.denbi.de/support/` · SimpleVM wiki →
  `{{ extra.simplevm_wiki_link }}` · Training material (de.KCD) →
  `https://datenkompetenz.cloud/training/`
- **de.NBI Cloud:** Website home → `https://cloud.denbi.de/` · Apply for a
  project → `https://cloud.denbi.de/register/` · Portal login →
  `https://cloud.denbi.de/portal/` · Service status →
  `https://status.cloud.denbi.de/`
- **Legal:** Terms of use → `https://cloud.denbi.de/about/policies/` · Imprint
  → `https://cloud.denbi.de/about/imprint/` · Cookie settings → `#__consent`
  (opens Material's consent dialog; same tab)
- **Legal line:** "© {current year} de.NBI" · "Edit this page on GitHub" (the
  page's edit link, opening GitHub's editor on `dev`, the branch pull
  requests target per `PULL_REQUEST_TEMPLATE.md`; `edit_uri` changes from the
  stale `blob/master/wiki/` to `edit/dev/wiki/`. The maintainer first chose
  `main`, then accepted `dev` when the PR template came up) · right-aligned text links "de.NBI" →
  `https://www.denbi.de/` and "GitHub" → `https://github.com/deNBI`.

This replaces the current `footer_links` row and the social icons (LinkedIn,
GitHub, YouTube, Wikipedia). Previous/next page links (`navigation.footer`)
stay off, as today.

### Dark mode (option B, "everything dark")

The page content keeps the existing slate tokens in `denbi.css`. Header and
footer follow the same dark palette:

- Quick access bar: a darker navy than the page (`#06121e` in the mockup),
  white links, cyan icons, muted label `#8fb3d6`, divider `--denbi-line`.
- Menu row: page background `--denbi-bg` (`#0d1b2a`), text `--denbi-ink`
  (light), current section and hover `--denbi-blue` (`#7cc0f5`), bottom line
  `--denbi-line`. Search field on `--denbi-bg-alt`.
- Apply button: unchanged website blue `#005aa9` with white text.
- Footer: `--denbi-bg-alt` background, light text, muted headings
  `--denbi-muted`.
- Logo: a light variant of `denbi-logo-color.svg` with the dark grey
  lettering (`#231F20`, `#58595B`, `#929497`) recoloured to light tones. Keep
  the blue, cyan and magenta marks. Switch between the two logos with the
  colour scheme.
- Funder and partner logos: official logos must not be recoloured. The
  BMFTR logo sits on a small white panel (rounded `--radius`, a few px
  padding) in both modes; in light mode the panel has a thin `--denbi-line`
  border (maintainer's request). The EU and ELIXIR logos switch to their
  official negative (white-lettering) versions, and the LS Login badge stays
  as is (see "Logos"). This is my call, following the builder check.

Light mode looks exactly like the website.

## Logos

Store them in `wiki/assets/images/partners/` and give each one an `alt` text
naming the organisation. Source files:

| Logo | Light mode | Dark mode | Source |
|---|---|---|---|
| BMFTR ("With funding from the: Federal Ministry of Research, Technology and Space") | as is | on light panel | `https://datenkompetenz.cloud/media/original_images/BMFTR_en_DTP_CMYK_gef_durch.jpg` (CMYK JPEG; convert to sRGB PNG/WebP without changing the artwork) |
| EU NextGenerationEU ("Funded by the European Union") | English horizontal positive (`EN_Funded_by_the_European_Union_RGB_POS.png`) | English horizontal negative (`..._RGB_NEG.png`) | European Commission download centre, `https://ec.europa.eu/regional_policy/information-sources/logo-download-center_en` (`nextgenerationeu_en.zip`). de.KCD uses the German vertical version; English (the wiki's language) and horizontal (for the compact logo row) are my calls |
| ELIXIR | `ELIXIR_logo_standard.svg` (orange + dark grey `#4D4848` lettering) | `ELIXIR_logo_negative_orange.svg` (orange + white lettering) | Official SVGs supplied by the maintainer (`~/Downloads/ELIXIR_logo_standard(1).svg`, `~/Downloads/ELIXIR_logo_negative_orange(1).svg`). Checked: no scripts or external references. The all-white `negative_white` variant is not used. Commit without the `(1)` in the file names |
| LS Login (LS AAI) | as is | as is (the badge has its own light background and cyan border, so it needs no panel) | `https://www.lifescience-ri.eu/wp-content/uploads/2025/09/login-grey-wide.jpg.png` (450×100 PNG, from https://www.lifescience-ri.eu/life-science-login/) |

Size: the same logo height as the website's footer funders (48px).

Follow-up outside this repo (maintainer's note): on the website, the EU
notice should appear only once in the footer, and ELIXIR and LS AAI could
move to a collaboration section. That's for `deNBI/landing_page`, not this
change.

## Constraints

- MkDocs Material 9.7.7 and pymdown-extensions 11.0.2, as pinned in
  `pyproject.toml` (matching the production image mkdocswebhook 3.9.7).
  Implement with theme overrides in `wiki/overrides/` (`main.html` and
  overridden partials such as `header.html`, `tabs.html`, `footer.html`) and
  CSS in `wiki/assets/css/`. Do not fork the theme.
- Links and labels live in `config.yml` under `extra:` (for example
  `extra.quick_links` and `extra.footer_columns`), so they can be updated by
  hand without editing templates. `config_local.yml` inherits them.
- Production is served under `https://cloud.denbi.de/wiki/`. Links to the
  website are absolute URLs.
- Icons: copy the five Material Symbols SVGs the quick access bar uses
  (`login`, `menu_book`, `dns`, `campaign`, `support_agent`) from the website,
  with its `SOURCE.txt`. Material for MkDocs bundles Material Design Icons,
  not Material Symbols, so they would not look identical.
- Accessibility at the level of the website: a skip link, a labelled `<nav>`
  for quick access ("Quick access"), `aria-current="true"` on the Wiki link and
  the current section (both mark the current item in a set, not the exact
  page; the maintainer confirmed this), contrast following the "cyan is a fill
  only" rule in `denbi.css`, and full keyboard use of search and the toggle.
- Must work at phone width without horizontal scrolling. The sections show in
  the menu row from 76.25em (1220px), the breakpoint where Material's sidebar
  becomes the lifted section sidebar. Below that, the menu row falls back to
  Material's drawer, which already holds the sections. The maintainer accepted
  this. The quick access bar stays visible with icons only. "Apply for a
  project" shortens to "Apply" below 900px, the website's mobile breakpoint.
- The `htmlproofer` check must keep passing.
- Local preview: `uv run mkdocs serve -f config_local.yml`.

## Release

The maintainer has decided that the wiki and the website redesign
(`deNBI/landing_page` `feat/cloud-redesign`) are both reviewed internally
first, then go live together. Consequences for the build:

- The work stays on feature branches and is not merged to `dev`, `staging` or
  `main` until the joint release is agreed.
- The internal review needs a preview that works without the production
  container: `uv run mkdocs serve -f config_local.yml` (or a static
  `mkdocs build` of it) must show the full new header and footer.
- No feature switch between the old and new header is needed.

## Left to the builder

- Exact markup and how the Material partials are split, as long as search,
  the palette toggle, instant loading and consent keep working.
- Whether the quick access bar scrolls away while the menu row stays sticky.
  Mirror what the website does on `feat/cloud-redesign`.
- Spacing and the remaining breakpoints. Copy the values from `cloud.css`
  where they exist.
- Whether "Concept" stays a sub-group inside OpenStack (expected: yes), and
  whether the home page shows the "Getting started" sidebar.
- The exact shade of the dark quick access bar, if `#06121e` does not meet
  contrast against the cyan icons.
