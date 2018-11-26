## Development Setup

The markdown files in this repo are visualized using [mkdocs-material](https://squidfunk.github.io/mkdocs-material/specimen/).
In the config.yaml you will find a list of all installed markdown extensions. You can find the documentation [here](https://squidfunk.github.io/mkdocs-material/extensions/admonition/).

### Docker

Use the Environment which will also be used in production.

~~~BASH
docker run -it -v "$(pwd)/wiki:/srv_root/docs/wiki" -v "$(pwd)/config.yml:/config.yml" -p "8000:8000"  --entrypoint="mkdocs" denbicloud/mkdocswebhook:2.0.0 serve -f /config.yml --dev-addr 0.0.0.0:8000
~~~

### Local

Please install the libraries used in the production instance:
https://github.com/deNBI/mkdocsWebhook/blob/master/Dockerfile#L4

~~~BASH
mkdocs serve -f config_local.yml
~~~
