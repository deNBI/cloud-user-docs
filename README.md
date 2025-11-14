## Development Setup

The markdown files in this repo are visualized using 
[mkdocs-material](https://squidfunk.github.io/mkdocs-material/specimen/).
In the config.yaml you will find a list of all installed markdown extensions. 
You can find the documentation 
[here](https://squidfunk.github.io/mkdocs-material/extensions/admonition/).


### Docker

Use the Environment which will also be used in production.

~~~BASH
docker run -it -v "$(pwd):/srv_root/docs"  -p "8000:8000" --env ENABLED_HTMLPROOFER=True --entrypoint="mkdocs"  quay.io/denbicloud/mkdocswebhook:3.8.0 serve -f /srv_root/docs/config.yml   --dev-addr 0.0.0.0:8000
~~~

Or turn off the HTML Proffer for faster startup:

~~~BASH
docker run -it -v "$(pwd):/srv_root/docs"  -p "8000:8000" --env ENABLED_HTMLPROOFER=False --entrypoint="mkdocs" quay.io/denbicloud/mkdocswebhook:3.8.0 serve -f /srv_root/docs/config.yml   --dev-addr 0.0.0.0:8000
~~~

### Local

Please install the libraries used in the production instance:
https://github.com/deNBI/mkdocsWebhook/blob/master/Dockerfile#L4

For a quick start you can also use pip to install both mkdocs and mkdocs-material:

~~~BASH
pip install mkdocs
pip install mkdocs-material
~~~

~~~BASH
mkdocs serve -f config_local.yml
~~~

### Text writing plugin for JetBrains IDEs

The [Grazie Professional plugin](https://plugins.jetbrains.com/plugin/16136-grazie-professional) can be used,
to ease text editing of this repository.
It allows you to utilize styleguides and gives you suggestions while writing.
For the [rephrasing and synonymization feature](https://plugins.jetbrains.com/plugin/16136-grazie-professional/docs/rephrasing-and-synonymization.html) you need to enable the processing via Grazie Cloud.

