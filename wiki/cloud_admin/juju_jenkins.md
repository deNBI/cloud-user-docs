## Deploy and configure jenkins and haproxy with JuJu

The following instructions have been used to setup Jenkins and Haproxy using [JuJu](https://jujucharms.com) in the de.NBI Cloud.
It has been tested in the Bielefeld Cloud Compute Center but should be applicable with little modifications on all
de.NBI Cloud compute centers.

## Setup juju client 

First we have to set up the juju client in a VM in OpenStack, so it has full network access to
newly spawned VMs without assigning a floating IP.

```
sudo add-apt-repository -yu ppa:juju/stable
sudo apt install juju
```

### Add cloud config

In the next step we need to configure our cloud setup. Therefore we create the
following config file `cebitec.yaml`:

```yaml
clouds:
  cebitec:
    type: openstack
    auth-types: [ userpass, access-key ]
    regions:
      Bielefeld:
        endpoint: https://openstack.cebitec.uni-bielefeld.de:5000/v3/

```
and run

```
juju add-cloud cebitec -f ./cebitec.yaml

```

### Add login credentials

To spawn VMs, juju must be able to login to OpenStack.
So add your credentials in a config file `cebitec-creds.yaml` like this

```yaml
credentials:
  cebitec:
    <credential name (e.g. username)>:
      auth-type: userpass
      username: <username>
      password: <password>
      tenant-name: <project>

```

and add them with

```
juju add-credential cebitec -f ./cebitec-creds.yaml

```

### Add image metadata

In order to use an image, juju needs to create some metadata for it first.
In this example we add the current xenial image.

We create a directory for metadata with the following command:

```
mkdir -p ~/juju/images
```

Now we add metadata for the xenial image

```
juju metadata generate-image -d ~/juju -i febceb9a-fb0f-4f1c-ad06-8caf6340de64 -s xenial -r Bielefeld -u https://openstack.cebitec.uni-bielefeld.de:5000/v3/

```

where the image ID in OpenStack has to be specified with the `-i` and the release name (series) with `-s`.

## Deploy the juju controller

Basically, this is just `juju bootstrap`. Because we use private cloud, we have
to specify the location of the image metadata with `--metadata-source`.

```
juju bootstrap --metadata-source ~/juju cebitec

```

If there are multiple networks available for your project, choose the right one
with the `--config network=<network id>` parameter.

## Deploy jenkins and haproxy

After deploying a juju controller it is possible to define a juju model in two yaml files.

- The first file describes the construction of the juju model 

- This model.yaml file creates 1 jenkins machine with docker installed and 1 haproxy machine.

- It also configures ssl termination with the files `ssl.key` and `ssl.crt`. 

```yaml
services:
  jenkins:
    charm: "cs:jenkins"
    num_units: 1
    options:
      password: <passwort>
      install_keys: 0EBFCD88
      install_sources: https://download.docker.com/linux/ubuntu xenial stable
      extra_packages: docker-ce
  haproxy:
    charm: "cs:haproxy"
    num_units: 1
    expose: true
    options:
      ssl_key: include-base64://ssl.key
      ssl_cert: include-base64://ssl.crt
relations:
  - - "jenkins:website"
    - "haproxy:reverseproxy"
``` 

!!! Note
    Do not forget to set a passwort in the options section of jenkins
    
To deploy jenkins and haproxy you have to execute the following command:

```BASH
juju deploy model.yaml
```


The second file configures our already deployed haproxy. It sets the exposed port of our setup to 443.

```yaml
- service_name: jenkins
  service_host: "0.0.0.0"
  service_port: 443
  crts: [DEFAULT]
  service_options:
      - balance leastconn
      - reqadd X-Forwarded-Proto:\ https
  server_options: maxconn 100 cookie S{i} check
``` 
to apply this configuration you need to run 

```BASH
juju config haproxy services=@hconfig.yaml
```

All possible options can be found at the charm websites under configuration [haproxy-charm](https://jujucharms.com/haproxy/).

## Run custom commands

It is possible to run custom commands with juju, using the run command:

```BASH
juju run  "<command>"  --machine <machine number>
```

The command below sets the docker group on machine 34:

```BASH
juju run "sudo usermod -aG docker $USER "  --machine  34
```

## Further Reading

* [Juju haproxy](https://jujucharms.com/haproxy/)

* [Juju jenkins](https://jujucharms.com/jenkins/)
 
# Optional steps

## Edit and push existing juju charm
This will describe how to push a charm to your repository and add layers to it.


## Prerequisite
An [ubuntu one](https://login.ubuntu.com) account is needed to upload your own charm.
```
sudo apt-get install charm
``` 
to install the charm software

## Download charm

Download the charm you want to edit from the charmstore by pressing Download .zip.

Now extract the zip file and open a terminal in the charm folder.

## Edit charm
If you want to add layers (for example [docker-layer](https://jujucharms.com/new/u/lazypower/docker)) to the charm you have to add
```includes: ['layer:docker']```  to the layer.yaml file. This will install docker+docker-compose to your charm.

!!! Note
    If you add the dockerlayer to your charm you dont need to add the docker-ce installation in your model.yaml


By editing the config.yaml you can adapt the charm description.

## Build charm
use:
```
charm build
cd builds/<charm-name> 
```
to generate code for the new layer and go into the ```builds/<charm name>``` folder with the terminal.

## Push charm and grant rights

You can now edit the files as needed and deploy the charm lokally with:
```
juju deploy <path to local charm>
```
and
```
charm push <path to local charm> 
```
to push it into your juju repository.

```
charm grant <charm url> everyone 
```
To make the charm accessible to all users.

Now you can deploy your charm by using the charm url in your model.yaml

## Adding jenkins user to dockergroup


To add the jenkins user by default to the docker group add the import:
 `from subprocess import check_call `
at the top and the command
 `check_call(['usermod', '-aG', 'docker', 'jenkins'])`
below the line: users = Users() in the <charm>/reactive/jenkins.py file

