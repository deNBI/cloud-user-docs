# de.NBI cloud at Bielefeld University

The Bielefeld cloud site currently has OpenStack Queens installed. That means that the general descriptions with 
screenshots based on OpenStack Newton differs from our installation. 

## Contact
The de.NBI cloud team in Bielefeld can be contacted via email: os-service(at)cebitec.uni-bielefeld.de


## Entrypoint
The OpenStack Dashboard as main entry point to the de.NBI Cloud Bielefeld is available 
at [https://openstack.cebitec.uni-bielefeld.de](https://openstack.cebitec.uni-bielefeld.de).

## Endpoints

You can get an up-to-date list of API endpoints of the available services using the dashboard or 
the OpenStack command-line tool (`openstack endpoint list`).

## Login
The Bielefeld cloud site supports login using Elixir AAI via OpenID Connect or default Keystone credentials. 
Using Elixir AAI is the preferred way for all cloud users and the only way for non-cloud users not working 
at Bielefeld university. 


## Network

The Bielefeld cloud currently has 3 different _external_ networks available.

- external
- external-service
- cebitec

### external

The external network is a publicly available network. There are no limitations from our side and it is the 
preferred network if you don't have access to the Bielefeld university LAN. 

### external-service

The external-service network is a public network that is restricted to ssh, http and https. It should only 
be used for (web-)services running in the cloud. Each IP address must be activated before usage.

!!! warning "Warning"
    In general this network shouldn't be used, ask cloud support if unsure.

### cebitec

The cebitec network is a non-public _external_ network, that can only be used from the Bielefeld university LAN. 
However, since this network represents a non-public ip address range, it is possible to have more than one in 
use at the same time. The access is limited to SSH, HTTP and HTTPS. Access to the world is only possible using 
the CeBiTec Proxy and only for HTTP, HTTPS and FTP.

```
export http_proxy=proxy.cebitec.uni-bielefeld.de:3128
export https_proxy=proxy.cebitec.uni-bielefeld.de:3128
export ftp_proxy=proxy.cebitec.uni-bielefeld.de:3128
```

### MTU settings

We make use of a network virtualization technology called Virtual Extensible LAN (VXLAN). The MTU value provided 
to the network interfaces is  1450 and therefore differs from an expected default *value* (e.g. 1500). You have to 
consider this if running docker or any other container technology.

## Images

We provide some preconfigured cloud images on top of the Ubuntu LTS (18.04 and 20.04) and Debian (10). These 
images are able to run on other cloud sites without any further modifications and come with a 
script `/usr/local/bin/de.NBI_Bielefeld_environment.sh` that adapts a running instance to 
the cloud site Bielefeld:

- set proxy for environment, apt and docker if necessary
- make use of apt-mirror

### Ubuntu apt mirror

We run an apt mirror for Ubuntu LTS releases (18.04 and 20.04) to speed up package download. The mirror is available 
at the Bielefeld cloud site through the external (http[s]://apt-cache.bi.denbi.de:9999 or http://129.70.51.2:9999) and c
ebitec (http://172.21.40.2:9999) network.
This mirror is synced every midnight with the official Canonical repositories.

## Object storage

The storage backend used by the Bielefeld cloud site is powered by [Ceph](https://www.ceph.com). The Object storage 
endpoint provides API access via SWIFT and S3. The latter should be preferred due to better performance.
You can find a tutorial [here](../Tutorials/ObjectStorage/index.md) on how to use this service.

## Protection against loss of data

Users should be aware, that instances are ephemeral. This means, that instances can go offline for various
reasons. This is most likely due to hardware issues on the hypervisor. Users can prepare against this
by storing their data in the storage infrastructure of this compute center. For this you can
use Snapshots and Volumes. This data is stored redundantly on our Ceph Cluster three times on different
locations of the cloud-center. Beware that this does not act as a backup. If you want true backups (which
are independent of this cloud-center), you have to copy your data to a safe location, like an external harddrive,
for yourself. We do our best to prevent any data loss, but we can't guarantee that 100%.
Here is a quick overview about our solutions for storing data:

| Data Location | Description | Performance |
| ------------- | ----------- | ----------- |
| Root Disk     | The root disk of an instance is hosted on a RAID10 backend. This means that data is safe against single harddrive failures. However, if the hypervisor itself goes bad your data will be also completely unavailable. | Fast |
| Ephemeral Disk | Some flavors provide an extra disk called "ephemeral disk". While this storage is practical for most use-cases it is also the most unsafe one. They are **not** included in Snapshots and should be used for temporarily used data. | Fast |
| Volumes       | Volumes are stored redundantly in our Ceph-Storage. Since volumes are network-backed storage, random read/write operations performance is significantly slower than using the local disk space. Volumes offer a great solution for storing persistent data since volumes can be swapped to different instances. | Medium - Fast |
| S3 Object Storage | This data is also stored in our Ceph-Storage just like volumes. Access to this data is completely independent from instances since access is done via regular HTTPS. Therefore data in S3 is safe against any hypervisor issues. Performance heavily depends on the client used to access the object storage. A single-threaded connection is slow but can heavily speed up using multiple connections retrieving different chunks of the same object. Pushing data is much slower than retrieving data. | Slow - Fast |


## Server Groups for optional performance gains

Our OpenStack cluster consists of multiple compute nodes hosting all running instances. Some applications
can benefit if you schedule the instances of your project on as many different compute nodes as possible.

- Distributed systems (like HPC, databases...) can get a significant performance gain.
- Spreading instances over several compute nodes increases the availability when running a high availability setup. 

This can be achieved with *Server Groups*. Server Groups act as a "container" for instances and describe 
a "policy" on how those instances should be scheduled across the OpenStack Compute nodes.

In order to create such Server Group, login to the OpenStack Dashboard and navigate to Compute -> Server Groups. 
Afterwards click on *Create Server Group*:
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

It is recommended to use the "soft" variant. Otherwise, instances can fail to start when they would violate 
the more strict policy options.

Afterwards the creation of a new Server Group, you can add instances to it when you are creating them. 
It's not possible to add already running instances to a Server Group since they are already scheduled.
On the *Server Groups* tab, add the group by clicking on the small up-arrow:
![sg_screen3](img/bielefeld/sg_screen3.png)

Afterwards, the scheduling of this instance will respect your selected Server Group policy.


## Application Credentials (use OpenStack API)

In order to access the OpenStack Cloud via command-line tools, you need to source a so called rc file as 
described [here](https://cloud.denbi.de/wiki/Tutorials/ObjectStorage/#retrieving-access-credentials).
However, the standard procedure does not work on all Cloud locations. Executing `source` on the 
downloaded rc file prompts for a password. This password **is not the same** you have used when 
authenticating to ELIXIR in order to access the OpenStack Dashboard.

Internally, OpenStack does not set a local password for your ELIXIR-ID, since it does not need to 
hence OpenStack confirms your authorization separately via ELIXIR AAI.
However, the commandline-tools can only function with a set local password. Prior to the new 
OpenStack release, users had to contact the cloud site administrators in order for them to set an 
explicit local password and send it back to the user via encrypted mail or de.NBI vault service. 

Luckily, there is a new feature since OpenStack Rocky where users are able to set their own *local* 
credentials via the dashboard.

Log in to the OpenStack Dashboard as usual, on the left side navigate to Identity -> Application 
Credentials and create a new credential set:
![ac_screen1](img/bielefeld/ac_screen1.png)

Afterwards, you have to specify your new credential set. You can leave the 'secret' field blank, 
OpenStack will autogenerate a long and cryptic password string afterwards. Of course you can also 
provide your own secret.
**Warning: The secret field is not hidden in the browser!**. Afterwards click on *Create Application Credential*:
![ac_screen2](img/bielefeld/ac_screen2.png)

In the new window, you can directly download a generated rc file. Make sure that you explicitly 
click on *Close* afterwards, otherwise the credential won't be saved:
![ac_screen3](img/bielefeld/ac_screen3.png)


After the credential has been downloaded to your favourite location,
you can simply source the file with:

```
#Depends on your location.
source ~/Downloads/<NAME OF RC FILE>
```

Now you can use the openstack commandline tools.

### Note

Application credentials are currently not supported by all applications or development kits accessing the 
Openstack API. In this case users have to contact the cloud site administrators in order for them to set 
an explicit local password.

## DNS as a Service

Attaching a floating ip to an instance automatically creates an A record in our public nameserver.
The A record will be generated according to the following scheme:

`<INSTANCE_NAME>.<PROJECT_NAME>.projects.bi.denbi.de`

Therefore, you can reach you instance (via SSH) not only by the numeric floating IP, but also by name. 

Detaching the floating IP will also delete the A record.

## (Information) Security

Our [information security policy (german language)](assets/bielefeld/informationssicherheitsleitlinie.md)  
ensures that we follow defined protocols and procedures.

### Clock synchronisation

Our cloud infrastructure and user virtual machines are clock synchronised using the Network Time Protocol (NTP).

### Information security incidents

If users become aware of a security incident or notice an abnormal behaviour of their instances (e.g. unexpected high CPU 
load or high network traffic without actively running anything), they should immediately contact 
the cloud administrators (os-service@cebitec.uni-bielefeld.de). The administrators will assist in isolating
the affected instances from the public network and will (with the owner's consent) start a basic forensic analysis.
Depending on the analysis results a security incident report is written and the security incident 
officer of Bielefeld university is informed. If any personal data is affected, the data security officer 
is also consulted.

### Cryptography

We use cryptographic methods to protect user data stored on our infrastructure:

- Client connections to our OpenStack Dashboard and Openstack API 
  are encrypted using TLS
- Local disks of instances are located on encrypted devices (LUKS).
- Cloud storage  is LUKS encrypted (work in progress)

## Known Problems

Our current setup has some known problems.

- Suspending and Shelving instances has been disabled for regular users. Please use the snapshot 
  functionality in order to save up on resources.
- Policy problems when using the dashboard object storage UI. However, the cmdline access works.
