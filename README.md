## Development Setup

The markdown files in this repo are visualized using 
[mkdocs-material](https://squidfunk.github.io/mkdocs-material/specimen/).
In the config.yaml you will find a list of all installed markdown extensions. 
You can find the documentation 
[here](https://squidfunk.github.io/mkdocs-material/extensions/admonition/).


### Docker

Use the Environment which will also be used in production.

~~~BASH
docker run -it -v "$(pwd):/srv_root/docs"  -p "8000:8000" --env ENABLED_HTMLPROOFER=True --entrypoint="mkdocs"  oci.bi.denbi.de/denbicloud/mkdocswebhook:3.9.7 serve -f /srv_root/docs/config.yml   --dev-addr 0.0.0.0:8000
~~~

Or turn off the HTML Proffer for faster startup:

~~~BASH
docker run -it -v "$(pwd):/srv_root/docs"  -p "8000:8000" --env ENABLED_HTMLPROOFER=False --entrypoint="mkdocs" oci.bi.denbi.de/denbicloud/mkdocswebhook:3.9.7 serve -f /srv_root/docs/config.yml   --dev-addr 0.0.0.0:8000
~~~

### Local

Dependencies are managed with [uv](https://docs.astral.sh/uv/) and pinned to the versions in the
[production image](https://github.com/deNBI/mkdocsWebhook/blob/master/Dockerfile).
`config_local.yml` inherits all settings from `config.yml` and only replaces the container paths.

~~~BASH
uv run mkdocs serve -f config_local.yml
~~~

When the production image is updated, update the pins in `pyproject.toml` with `uv add`.

Run the checks, which build the wiki and inspect the generated pages, with:

~~~BASH
uv run pytest
~~~

### Header and footer

The header and footer follow the [de.NBI Cloud website](https://cloud.denbi.de/). Their links and logos
live in `config.yml` under `extra:` (`quick_links`, `apply`, `footer_columns`, `footer_logo_groups`,
`footer_legal_links`). The website's navigation is edited in its CMS, so update these values by hand
when it changes. Templates are in `wiki/overrides/partials/`, styles in `wiki/assets/css/chrome.css`,
and the sources of the partner logos in `wiki/assets/images/partners/SOURCE.txt`.

### Text writing plugin for JetBrains IDEs

The [Grazie Professional plugin](https://plugins.jetbrains.com/plugin/16136-grazie-professional) can be used,
to ease text editing of this repository.
It allows you to utilize styleguides and gives you suggestions while writing.
For the [rephrasing and synonymization feature](https://plugins.jetbrains.com/plugin/16136-grazie-professional/docs/rephrasing-and-synonymization.html) you need to enable the processing via Grazie Cloud.

