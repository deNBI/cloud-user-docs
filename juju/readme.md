## Deploy and configure jenkins and haproxy with juju

## Setup jujuj client 

First we need to up the juju client in a VM inside openstack, so it has full network access to
newly spawned VMs without assining a floating IP.

First install juju via apt with

```
sudo add-apt-repository -yu ppa:juju/stable
sudo apt install juju
```

### Add cebitec cloud

In the next step, we need to add our cloud to juju. Therefore we create the
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
and then run

```
juju add-cloud cebitec -f ./cebitec.yaml

```

### Add login credentials

To spawn VMs, juju must be able to login to openstack.

To add credentials, again create a config file `cebitec-creds.yaml` like this

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


To use an image, juju needs to create some metadata for it first.
This needs to be done for every image, you want to use with juju.
In this example we add the current xenial image.

First we create a directory for the metadata:

```
mkdir -p ~/simplestreams/images

```

Now we add metadata for the xenial image

```
juju metadata generate-image -d ~/simplestreams -i febceb9a-fb0f-4f1c-ad06-8caf6340de64 -s xenial -r Bielefeld -u https://openstack.cebitec.uni-bielefeld.de:5000/v3/

```
where the image ID in opsntack has to be specified with the `-i` switch and the release name (series) with `-s`.

## Deploy the juju controller

Basically, this is just `juju bootstrap`. Because we use private cloud, we have
to specify the location of the image metadata with `--metadata-source`.

```
juju bootstrap --metadata-source ~/simplestreams cebitec

```

If there are multiple networks available for your project, choose the right one
with the `--config network=<network id>` parameter.

## Deploy jenkins and haproxy

After deploying a juju controller it is possible to define a juju model in two yaml files.

- The first file descibes the construction of the juju model 
- This model.yaml file creates 1 jenkins machine and 1 haproxy machine. 
```yaml
applications: 
  jenkins: 
    charm: "cs:jenkins"
    num_units: 1
  haproxy: 
    charm: "cs:haproxy"
    num_units: 1
    expose: true
relations: 
  - - "jenkins:website"
    - "haproxy:reverseproxy"
``` 

-   The second file configures the applications.
-   This deploy.yaml file sets the password for the jenkins webapp and adds a ssl certificate and key to the haproxy setup.
```yaml
applications:
  jenkins:
    options:
      password: <password>
  haproxy:
    options:
      ssl_key: include-base64://ssl.key
      ssl_cert: include-base64://ssl.crt
``` 
-  All possible options can be found at the charm websites under configuration [haproxy-charm](https://jujucharms.com/haproxy/).

- Now you can deploy the juju model and configurations with the following command.

`juju deploy model.yaml --overlay=deploy.yaml`