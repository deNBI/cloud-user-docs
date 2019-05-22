# de.NBI cloud at Bielefeld University

The Bielefeld cloud site currently has Openstack Queens installed. That means that the general descriptions or screenshots based on Openstack Newton differs from our installation. 

## Contact
The de.NBI cloud team in Bielefeld can be contacted via email: os-service(at)cebitec.uni-bielefeld.de


## Entrypoint
The entry point of the Bielefeld location of the de.NBI cloud  - the Openstack dashboard is available at [https://openstack.cebitec.uni-bielefeld.de]().

## Endpoints

You can get an up to date list of API endpoints of the following services using the dashboard or the OpenStack commandline tool (`> openstack endpoint list`).

| Service Name | Service Type |
|--------------|--------------|                                                
| swift        | object-store |
| nova         | compute      |
| cinderv2     | volumev2     |
| keystone     | identity     |
| glance       | image        |
| neutron      | network      |
| cinder       | volume       |

## Login
The Bielefeld cloud site supports login using Elixir AAI via OpenID Connect or default Keystone credentials. Using Elxir AAI is the prefered way for all cloud users and the only way for non cloud users not working at the Bielefeld university. 


## Network

The Bielefeld cloud currently has 3 different _external_ networks available.

- external
- external-service
- cebitec

### external

The external network is a public available network. There are no limitations from our side and it is the preferred network if you don't have access to the Bielefeld university LAN. 

### external-service

The external-service network is a public network that is restricted to ssh, http and https. It should only be used for (web-)services running in the cloud. Each IP address must be activated before usage.

!!! warning "Warning"
    In general this network shouldn't be used, ask cloud support if unsure.

### cebitec

The cebitec network is a non-public _external_ network, that can only be used from the Bielefeld university LAN. However, since this network represents a non-public ip address range, it is possible to have more than one in use at the same time. The access is limited to ssh, http and https. Access to the world is only possible using the CeBiTec Proxy and only for http, https, and ftp.

```
export http_proxy=proxy.cebitec.uni-bielefeld.de:3128
export https_proxy=proxy.cebitec.uni-bielefeld.de:3128
export ftp_proxy=proxy.cebitec.uni-bielefeld.de:3128
```

If you use our official images, the CeBiTec network will be detected automatically and the proxy settings will be set by an systemd service.

!!! note "Note" 
    It takes up to one minute after a VM is running to detect the network and set the proxy settings.

## Images
We provide some preconfigured Cloud images on top of the Ubuntu LTS releases (16.04 and 18.04). This images are patched to set the proxy settings if an cebitec network is detected. These image run without any further modifications on other cloud sites aswell.

## Object storage
The storage backend used by Bielefeld cloud site is powered by [Ceph](https://www.ceph.com). The Object storage endpoint provides API access via SWIFT and S3. The latter should be preferred due to better performance.



## Application Credentials (use OpenStack SDK)
In order to access the OpenStack Cloud via commandline tools, you need to source a so called rc file as described [here](https://cloud.denbi.de/wiki/Tutorials/ObjectStorage/#retrieving-access-credentials).
However, the standard procedure does not work on all Cloud locations. Executing `source` on the downloaded rc file prompts for a password. This password is not the same you have used when authenticating to ELIXIR in order to access the OpenStack Dashboard.

Internally, OpenStack does not set a local password for your ELIXIR-ID, since it does not need to hence OpenStack confirms your authorization seperately via ELIXIR AAI.
However, the commandline-tools can only function with a set local password. Prior to the new OpenStack release, users had to contact the cloud site administrators in order for them to set an explicit local password and send it via encrypted mail back to the user.

Luckily, there is a new feature in OpenStack Rocky where the user is able to set it's own *local* credentials via the dashboard.

Log in to the OpenStack Dashboard as usual, on the left side navigate to Identity -> Application Credentials and create a new credential set:
![ac_screen1](img/bielefeld/ac_screen1.png)

Afterwards, you have to specify your new credential set. You can leave the 'secret' field blank, OpenStack will autogenerate a long and cryptic password string afterwards. Of course you can also provide your own secret.
**Warning: The secret field is not hidden in the browser!**. Afterwards click on *Create Application Credential*:
![ac_screen2](img/bielefeld/ac_screen2.png)

In the new window, you can directly download a generated rc file. Make sure that you explicitly click on *Close* afterwards, otherwise the credential won't be saved:
![ac_screen3](img/bielefeld/ac_screen3.png)


After the credential has been downloaded to your favourite location,
you can simply source the file with:
```
#Depends on your location.
source ~/Downloads/<NAME OF RC FILE>
```

Now you can use the openstack commandline tools.



