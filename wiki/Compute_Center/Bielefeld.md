# de.NBI cloud at Bielefeld University

The Bielefeld cloud site currently has Openstack Queens installed. That means that the general descriptions or screenshots based on Openstack Newton differs from our installation. 

## Contact
The de.NBI cloud team in Bielefeld can be contacted via email: os-service(at)cebitec.uni-bielefeld.de


## Entrypoint
The entry point of the Bielefeld location of the de.NBI cloud  - the Openstack dashboard is available at [https://openstack.cebitec.uni-bielefeld.de]().

## Endpoints


| Service Name | Service Type |  URL |    
|--------------|--------------|------|                                                
| swift        | object-store | https://openstack.cebitec.uni-bielefeld.de:8080/swift/v1 |
| nova         | compute      | https://openstack.cebitec.uni-bielefeld.de:8774/v2.1/%(tenant_id)s |
| cinderv2     | volumev2     | https://openstack.cebitec.uni-bielefeld.de:8776/v2/%(tenant_id)s   |
| keystone     | identity     | https://openstack.cebitec.uni-bielefeld.de:5000/v3/            |
| glance       | image        | https://openstack.cebitec.uni-bielefeld.de:9292                    |
| neutron      | network      | https://openstack.cebitec.uni-bielefeld.de:9696                    |
| cinder       | volume       | https://openstack.cebitec.uni-bielefeld.de:8776/v1/%(tenant_id)s   |


(July 2018)

An up to date list of endpoints are available within the dashboard or can be fetched using the Openstack commandline tools.

```
> openstack endpoint list
```

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
The storage backend used by Bielefeld cloud site is powered by [https://www.ceph.com](Ceph). The Object storage endpoint provides API access via SWIFT and S3. The latter should be preferred due to better performance.

## Known Problems

Our current setup has some known problems.

- Login sometimes fails. The workaround is to create a new private browser window and login again.
- Create a router fails for non-admins, if a gateway is set. The workaround for this problem is to create a router without setting a gateway and  set the gateway and network bindings afterwards
- Dashboard shows admin panel (without any functionality) for normal user.
- Policy problems when using the dashboard object storage UI. However the cmdline access works.
