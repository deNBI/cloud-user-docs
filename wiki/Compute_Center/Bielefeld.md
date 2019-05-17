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
We provide some preconfigured Cloud images on top of the Ubuntu LTS releases (16.04 and 18.04). This images are patched to set the proxy settings if an  cebitec network is detected. These image run without any further modifications on other cloud sites aswell.

## Object storage
The storage backend used by Bielefeld cloud site is powered by [Ceph](https://www.ceph.com). The Object storage endpoint provides API access via SWIFT and S3. The latter should be preferred due to better performance.

## Known Problems

Our current setup has some known problems.

- Login sometimes fails. The workaround is to create a new private browser window and login again.
- Create a router fails for non-admins, if a gateway is set. The workaround for this problem is to create a router without setting a gateway and  set the gateway and network bindings afterwards
- Dashboard shows admin panel (without any functionality) for normal user.
- Policy problems when using the dashboard object storage UI. However the cmdline access works.



## DNS fix for instances using the CeBiTec Network (2019-05-17)

This guide describes a way to restore dns functionality for instances in the Bielefeld Cloud where instances are connected to the CeBiTec Network Gateway.
**Don't apply this guide to instances who are connected to the external network (eg. instances with floating IPs like 129.70.51.x)**,

In order to restore dns functionality, log-in to your project via the OpenStack Dashboard. And navigate on the left side to your network tab:
![Screen 1](img/bielefeld/screen1.png)

There you should see a list of all internal and external network. We are interested in the one which has an associated subnet, here for example *myNetwork*.
Select the associated network by clicking on it (2). Afterwards a new configuration should pop up:

![Screen 2](img/bielefeld/screen2.png)

Select the "Subnets" tab (1) and on the single subnet select "Edit Subnet" (2). A new window opens up:

![Screen 3](img/bielefeld/screen3.png)

Here, select the "Subnet Details" tab (1) and enter the IP of the DNS Name Server in the middle box like done in the screenshot (2).
Don't change anything else! Afterwards, save (3) the settings and your instances should receive the changes via DHCP automatically in a few moments.

You can also force this change on your instances:

```
# On Ubuntu 18.04
sudo netplan apply

# On Ubuntu 16.04
sudo dhclient -r
sudo dhclient
```

Afterwards, running instances should be able to resolve DNS again.

**WARNING: Since we are overriding the nameserver directly, we are bypassing any local DNS Nameservers. This means, that other instances in the same project are not resolveable anymore. This can break cluster applications (like Gridengine) who are connecting to their slaves via hostnames. Instances are still reachable via ip address as usual.**


If you create new instances in this project/network, it can happen that those instances have missing proxy settings. In order to fix this, connect to your new instance and issue the following command:

`sudo sh /usr/local/bin/de.NBI_Bielefeld_environment.sh`

Afterwards, log-out and log-in in order for the changes to take effect.


