## Deploy and configure jenkins and haproxy with juju

The following instructions have been used to setup jenkins using [JuJu](https://jujucharms.com) in the de.NBI Cloud.

## Setup jujuj client 

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

```
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

- This model.yaml file creates 1 jenkins machine and 1 haproxy machine.

- It also configures ssl termination with the files `ssl.key` and `ssl.crt`. 

```yaml
services:
  jenkins:
    charm: "cs:jenkins"
    num_units: 1
    options:
      password: <passwort>
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

The second file configures our deployed haproxy. It sets exposed port of our setup to 443.

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

All possible options can be found at the charm websites under configuration [haproxy-charm](https://jujucharms.com/haproxy/).
Now you can deploy the juju model and configurations with the following command.

## Run custom commands

It is possible to run custom commands with juju 

```BASH
juju config haproxy services=@haproxy_config.yaml
```

## Further Reading

* [Juju haproxy](https://jujucharms.com/haproxy/)

* [Juju jenkins](https://jujucharms.com/jenkins/)
