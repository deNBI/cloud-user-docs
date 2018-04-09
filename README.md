## Development Setup

### Docker

~~~BASH
docker run -it -v "$(pwd)/wiki:/srv_root/docs/wiki" -v "$(pwd)/config.yml:/config.yml" -p "8000:8000"  --entrypoint="mkdocs" denbicloud/mkdocswebhook serve -f /config.yml --dev-addr 0.0.0.0:8000
~~~

### Local

Please install the libraries used in the production instance:
https://github.com/deNBI/mkdocsWebhook/blob/master/Dockerfile#L4

~~~BASH
mkdocs serve -f config_local.yml
~~~
