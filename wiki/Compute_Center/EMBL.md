# de.NBI cloud at EMBL
EMBL OpenStack instance currently runs RHOSP 16.1, which is based on upstream OpenStack Train release.
You can find plenty of end-user documentation both from [RedHat](https://access.redhat.com/documentation/en-us/red_hat_openstack_platform/16.1/) 
and from [upstream openstack project](https://docs.openstack.org/train/user/).

## Contact
The de.NBI cloud team at EMBL can be contacted via denbi-requests(at)embl.de

## Entrypoint
The OpenStack Dashboard as main entry point to the EMBL de.NBI Cloud is available 
at [https://denbi.cloud.embl.de](https://denbi.cloud.embl.de).

## Endpoints
You can get an up-to-date list of API endpoints of the available services using the dashboard or 
the OpenStack command-line tool (`openstack endpoint list`).

## Login
LifeScience AAI federation is the preferred way to authenticate de.NBI users on EMBL cloud instance. Local keystone
authentication is also available upon request.

## Network
EMBL de.NBI cloud implements an external network on the public internet, together with a pool of public IPs available 
for your projects. Each project will be asigned at least one of these public IPv4 addresses. You will be able to set up 
internet facing services at ports of your choice (with a few exceptions). We're not providing DNS services but you're 
welcome to come up with your own DNS arrangemets for services you set up.

## Images
We provide a couple of default images for common linux distributions (CentOS, Debian, Ubuntu) and Windows (2012).

## Object storage
EMBL instance currently does not offer integrated object storage.

## Protection against loss of data
Be advised that instances are ephemeral. This means that when instances go offline (for any reason), data on their
ephemeral disks is lost. Users can prepare against this by using OpenStack Volumes, which store data persistently 
on the backend Ceph infrastructure.

Be advised that this is not a backup. If you want true backups, independent of this cloud-center, you have to copy 
your data to a safe location, like an external harddrive, yourself. We do our best to prevent any data loss, but 
we can't guarantee that 100%.

## Flavors
Besides standard OpenStack flavors (m1.\*) and de.NBI instances (de.NBI \*) we also provide flavors sized to align
optimally to the underlying hardware. They're named f1.optimal\* for CPU only instances and g1.optimal\* for gpu instances.
Please use them if you plan to run a compute heavy project.

## Happy computing!
