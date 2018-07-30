# OpenStack components

This article covers some of the underlying components of OpenStack. For using the denBI-Cloud, it is not really needed to understand the following topics. However, it could provide some interesting and technical information.

[OpenStack](http://openstack.org) is a free and open-source software platform for cloud computing, mostly deployed as an infrastructure-as-a-service (IaaS). The software platform consists of interrelated components that control diverse, multi-vendor hardware pools of processing, storage, and networking resources throughout a data center. Users either manage it through a web-based dashboard, through command-line tools, or through a RESTful API. OpenStack.org released it under the terms of the Apache License.

## OpenStack components

OpenStack has a modular architecture with various code names for its components.
The following image shows a very basic overview of the OpenStack architecture:

![Openstack_Overview](/img/User/openstackarchi.png)


### Compute (Nova)

OpenStack Compute (Nova) is a cloud computing fabric controller, which is the main part of an IaaS system. It is designed to manage and automate pools of computer resources and can work with widely available virtualization technologies, as well as bare metal and high-performance computing (HPC) configurations. KVM, VMware, and Xen are available choices for hypervisor technology (virtual machine monitor), together with Hyper-V and Linux container technology such as LXC.

It is written in Python and uses many external libraries such as Eventlet (for concurrent programming), Kombu (for AMQP communication), and SQLAlchemy (for database access). Compute's architecture is designed to scale horizontally on standard hardware with no proprietary hardware or software requirements and provide the ability to integrate with legacy systems and third-party technologies.

Due to its widespread integration into enterprise-level infrastructures, monitoring OpenStack performance in general, and Nova performance in particular, at scale has become an increasingly important issue. Monitoring end-to-end performance requires tracking metrics from Nova, Keystone, Neutron, Cinder, Swift and other services, in addition to monitoring RabbitMQ which is used by OpenStack services for message passing.

### Networking (Neutron)

OpenStack Networking (Neutron) is a system for managing networks and IP addresses. OpenStack Networking ensures the network is not a bottleneck or limiting factor in a cloud deployment, and gives users self-service ability, even over network configurations.

OpenStack Networking provides networking models for different applications or user groups. Standard models include flat networks or VLANs that separate servers and traffic. OpenStack Networking manages IP addresses, allowing for dedicated static IP addresses or DHCP. Floating IP addresses let traffic be dynamically rerouted to any resources in the IT infrastructure, so users can redirect traffic during maintenance or in case of a failure.

Users can create their own networks, control traffic, and connect servers and devices to one or more networks. Administrators can use software-defined networking (SDN) technologies like OpenFlow to support high levels of multi-tenancy and massive scale. OpenStack networking provides an extension framework that can deploy and manage additional network services—such as intrusion detection systems (IDS), load balancing, firewalls, and virtual private networks (VPN).

### Block Storage (Cinder)

OpenStack Block Storage (Cinder) provides persistent block-level storage devices for use with OpenStack compute instances. The block storage system manages the creation, attaching and detaching of the block devices to servers. Block storage volumes are fully integrated into OpenStack Compute and the Dashboard allowing for cloud users to manage their own storage needs. In addition to local Linux server storage, it can use storage platforms including Ceph, CloudByte, Coraid, EMC (ScaleIO, VMAX, VNX and XtremIO), GlusterFS, Hitachi Data Systems, IBM Storage (IBM DS8000, Storwize family, SAN Volume Controller, XIV Storage System, and GPFS), Linux LIO, NetApp, Nexenta, Nimble Storage, Scality, SolidFire, HP (StoreVirtual and 3PAR StoreServ families) and Pure Storage. Block storage is appropriate for performance sensitive scenarios such as database storage, expandable file systems, or providing a server with access to raw block level storage. Snapshot management provides powerful functionality for backing up data stored on block storage volumes. Snapshots can be restored or used to create a new block storage volume.

### Identity (Keystone)

OpenStack Identity (Keystone) provides a central directory of users mapped to the OpenStack services they can access. It acts as a common authentication system across the cloud operating system and can integrate with existing backend directory services like LDAP. It supports multiple forms of authentication including standard username and password credentials, token-based systems and AWS-style (i.e. Amazon Web Services) logins. Additionally, the catalog provides a queryable list of all of the services deployed in an OpenStack cloud in a single registry. Users and third-party tools can programmatically determine which resources they can access.

### Image (Glance)

OpenStack Image (Glance) provides discovery, registration, and delivery services for disk and server images. Stored images can be used as a template. It can also be used to store and catalog an unlimited number of backups. The Image Service can store disk and server images in a variety of back-ends, including Swift. The Image Service API provides a standard REST interface for querying information about disk images and lets clients stream the images to new servers.

Glance adds many enhancements to existing legacy infrastructures. For example, if integrated with VMware, Glance introduces advanced features to the vSphere family such as vMotion, high availability and dynamic resource scheduling (DRS). vMotion is the live migration of a running VM, from one physical server to another, without service interruption. Thus, it enables a dynamic and automated self-optimizing datacenter, allowing hardware maintenance for the underperforming servers without downtimes.

Other OpenStack modules that need to interact with Images, for example Heat, must communicate with the images metadata through Glance. Also, Nova can present information about the images, and configure a variation on an image to produce an instance. However, Glance is the only module that can add, delete, share, or duplicate images.[53]

### Object Storage (Swift)

OpenStack Object Storage (Swift) is a scalable redundant storage system. Objects and files are written to multiple disk drives spread throughout servers in the data center, with the OpenStack software responsible for ensuring data replication and integrity across the cluster. Storage clusters scale horizontally simply by adding new servers. Should a server or hard drive fail, OpenStack replicates its content from other active nodes to new locations in the cluster. Because OpenStack uses software logic to ensure data replication and distribution across different devices, inexpensive commodity hard drives and servers can be used.

In August 2009, Rackspace started the development of the precursor to OpenStack Object Storage, as a complete replacement for the Cloud Files product. The initial development team consisted of nine developers. SwiftStack, an object storage software company, is currently the leading developer for Swift with significant contributions from HP, Red Hat, NTT, NEC, IBM and more.

### Dashboard (Horizon)

OpenStack Dashboard (Horizon) provides administrators and users with a graphical interface to access, provision, and automation of cloud-based resources. The design accommodates third party products and services, such as billing, monitoring, and additional management tools. The dashboard is also brand-able for service providers and other commercial vendors who want to make use of it. The dashboard is one of several ways users can interact with OpenStack resources. Developers can automate access or build tools to manage resources using the native OpenStack API or the EC2 compatibility API.

### Orchestration (Heat)

Heat is a service to orchestrate multiple composite cloud applications using templates, through both an OpenStack-native REST API and a CloudFormation-compatible Query API.

### Telemetry (Ceilometer)

OpenStack Telemetry (Ceilometer) provides a Single Point Of Contact for billing systems, providing all the counters they need to establish customer billing, across all current and future OpenStack components. The delivery of counters is traceable and auditable, the counters must be easily extensible to support new projects, and agents doing data collections should be independent of the overall system.









Content of this page is largely based on [Wikipedia OpenStack](https://en.wikipedia.org/wiki/OpenStack) descriptions. Feel free to modify and extend these contents here as appropriate.''
