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
We make use of a network virtualization technology called Virtual Extensible Lan (VXLAN). The MTU value provided to the network interfaces is  1440 and therefor differs from an expected *value* (e.g. 1500). You have to consider this if running docker or any other container technology.


## Images
We provide some preconfigured cloud images on top of the Ubuntu LTS (16.04 and 18.04) and Debian (9). These images run without any further modifications on other cloud sites as well and come with a script `/usr/local/bin/de.NBI_Bielefeld_environment.sh` that adapt a running instance to the cloud site Bielefeld:

- set proxy for enviroment, apt and docker if necessary
- make use of apt-mirror

### Ubuntu apt mirror
We run an apt mirror for Ubuntu LTS releases (16.04 and 18.04) to speed up package download. The mirror is available from Bielefeld cloud site from the external (http[s]://apt-cache.bi.denbi.de:9999 or http://129.70.51.2:9999) and cebitec (http:172.21.40.2:9999) network.    

## Object storage
The storage backend used by Bielefeld cloud site is powered by [Ceph](https://www.ceph.com). The Object storage endpoint provides API access via SWIFT and S3. The latter should be preferred due to better performance.

## Known Problems

Our current setup has some known problems.

- Policy problems when using the dashboard object storage UI. However the cmdline access works.
