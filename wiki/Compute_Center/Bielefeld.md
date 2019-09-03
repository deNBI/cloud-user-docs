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

### MTU settings
We make use of a network virtualization technology called Virtual Extensible Lan (VXLAN). The MTU value provided to the network interfaces is  1450 and therefor differs from an expected *value* (e.g. 1500). You have to consider this if running docker or any other container technology.


## Images
We provide some preconfigured cloud images on top of the Ubuntu LTS (16.04 and 18.04) and Debian (9). These images run without any further modifications on other cloud sites as well and come with a script `/usr/local/bin/de.NBI_Bielefeld_environment.sh` that adapt a running instance to the cloud site Bielefeld:

- set proxy for enviroment, apt and docker if necessary
- make use of apt-mirror

### Ubuntu apt mirror
We run an apt mirror for Ubuntu LTS releases (16.04 and 18.04) to speed up package download. The mirror is available from Bielefeld cloud site from the external (http[s]://apt-cache.bi.denbi.de:9999 or http://129.70.51.2:9999) and cebitec (http:172.21.40.2:9999) network.  

## Object storage
The storage backend used by Bielefeld cloud site is powered by [Ceph](https://www.ceph.com). The Object storage endpoint provides API access via SWIFT and S3. The latter should be preferred due to better performance.


## Server Groups for optional performance gains
Our OpenStack cluster consists of many compute nodes which hosts all running instances. In some applications, it would be reasonable, when multiple instances of your project would be scheduled on as many different nodes as possible.

Distributed systems (like HPC, databases...) can gain a significant performance gain.

This can be achieved with *Server Groups*. Server Groups act as a "container" for instances and it describes a "policy" on how those instances should be scheduled across the OpenStack Compute nodes.

In order to create such Server Group, login to the OpenStack Dashboard and navigate to Compute -> Server Groups. Afterwards click on *Create Server Group*:
![sg_screen1](img/bielefeld/sg_screen1.png)

On the new screen, give this security group a name and assign the wanted affinity policy:
![sg_screen2](img/bielefeld/sg_screen2.png)

The policies are defined as following:

| Policy | Description |
|--------------|--------------|                                                
| affinity        | Force schedule all instances on one single compute node. |
| soft affinity         | Try to schedule all instances on a single compute node. Allow to violate the policy when there is not enough space on this single node.      |
| anti affinity     | Force schedule all instances as spread as possible on all compute nodes.     |
| soft anti affinity    | Try to schedule all instances as spread as possible on all compute nodes. Allow to violate this policy when there are not enough compute nodes with such capacity.     |

It is recommended to use the "soft" variant. Otherwise, instances can fail to start when they would violate the more strict policy options.

Afterwards the creation of a new Server Group, you can add instances to it when you are creating them. It's not possible to add already running instances to a Server Group since they are already scheduled. On the 
*Server Groups* tab, add the group by clicking on the small up-arrow:
![sg_screen3](img/bielefeld/sg_screen3.png)

Afterwards, the scheduling of this instance will respect your selected Server Group policy.


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


## Known Problems

Our current setup has some known problems.

- Policy problems when using the dashboard object storage UI. However the cmdline access works.


