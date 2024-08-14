# Documentation for the de.NBI Cloud Wiki

This repository contains the documentation for the de.NBI Cloud Wiki. If you want to contribute to the documentation, please follow the instructions below.

## Contributing

To contribute to the documentation:

1. fork this repository
2. clone your fork
3. create a feature branch with a concise but informative name
4. checkout your feature branch
5. make your changes, add and commit them
6. submit a pull request from your feature branch against the repository's `dev` branch.

Please check the [development setup](#development-setup) section for more information on how to set up the development environment and for more links to the mkdocs-material documentation.
The documentation is written in markdown, and you can use any text editor to make your changes.

### Adding a new page

Please check the existing pages to see if the content you want to add already exists. If it does not, you can add a new page under one of the existing categories (directories) below the `wiki` folder.

To add a new page, create a new markdown file in the `wiki` directory. See the existing markdown files for examples. 

To include the page in the navigation, edit the `config.yml` and `config_local.yml` file and add the new page to the `nav` section. Please check the existing pages listed in the `nav` section for examples.

### Editing an existing page

To edit an existing page, simply open the markdown file in the `wiki` directory and make your changes using markdown syntax.

### Adding images

To add images, please add your images to the `wiki/img` folder. You can then reference the images in your markdown files using the relative path to the image. See the `wiki/registration.md` file for an example.

## Development Setup

The markdown files in this repo are visualized using 
[mkdocs-material](https://squidfunk.github.io/mkdocs-material/specimen/).
In the config.yaml you will find a list of all installed markdown extensions. 
You can find the documentation 
[here](https://squidfunk.github.io/mkdocs-material/extensions/admonition/).


### Docker

Use the Environment which will also be used in production.

~~~BASH
docker run -it -v "$(pwd):/srv_root/docs"  -p "8000:8000" --env ENABLED_HTMLPROOFER=True --entrypoint="mkdocs" podman pull quay.io/denbicloud/mkdocswebhook:3.3.0 serve -f /srv_root/docs/config.yml   --dev-addr 0.0.0.0:8000
~~~

Or turn off the HTML Proffer for faster startup:

~~~BASH
docker run -it -v "$(pwd):/srv_root/docs"  -p "8000:8000" --env ENABLED_HTMLPROOFER=False --entrypoint="mkdocs" quay.io/denbicloud/mkdocswebhook:3.3.0 serve -f /srv_root/docs/config.yml   --dev-addr 0.0.0.0:8000
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

### Text writing plugin for Visual Studio Code

The [Code Spell Checker](https://marketplace.visualstudio.com/items?itemName=streetsidesoftware.code-spell-checker) plugin can be used to check spelling in markdown files.
