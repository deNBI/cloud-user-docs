## Networking

### Introdcution

Openstacks networking component is called Neutron. During the first steps of the quickstart guide it is shown how to build up a network using a single VM. This section will give some brief background information on openstack networking as well as some suggestions regarding the openstack installation in Giessen. Some of the details described in the following are shortened for the purpose of simplicity and better understanding. If you want and or need to get a deep understanding of openstack networking please refer to the official documentation.
[This](http://superuser.openstack.org/articles/everything-you-need-to-know-to-get-started-with-neutron-f90e2797-26b7-4d1c-84d8-effef03f11d2/) tutorial gives a short introduction to openstack networking based on a generic openstack installation using the command line client. In the following section of these parts are replicated using the horizon dashboard.
### Connecting VMs

To connect VMs to each other a network is reqiured. To create such a network in openstack it is necessary to first create a network and then associate a subnet with that network. The network acts like a VLAN whilst the subnet contains a block of IP adresses along with a certain configuration (e.g. DHCP settings).
To connect VMs to each other a network has to be created and associated with a subnet. To create a new network go to Project -> Network -> Networks and click on Create Network.

![Network overview](/img/User/network_start.png)

Enter some name for the network and click next. In the next form the subnet associated with the network is created. The following parts of the form have to be filled to create a basic subnet:

*  Subnet Name: Name of the subnet

*  Network Address: Adress space of the subnet in [CIDR](https://de.wikipedia.org/wiki/Classless_Inter-Domain_Routing) notation
The other options can be left on default.
Some words on the CIDR notation:
The CIDR notation defines a certain adress space inside the IPv4 space. Usually an IP block from a private IP subnet is used. In our case we will use the 10.2.0.0/16 net. This means that the IP addresses range from 10.2.0.1 to 10.2.0.254.

![Network first step](/img/User/network_form1.png)

After clicking next some details of the subnet can be configured:

*  Enable DHCP: Assign IPs to host using DHCP

*  Allocation Pools: Pool of IP adresses that can be used (for example 10.0.2.100, 10.0.2.150 means that only adresses ranging from 10.0.2.100 to 10.0.2.150 are used).

*  DNS Name Servers: DNS server for the specific subnet. Can be used to make machines accessible by using DNS instead of IP.

*  Host Routes: Routes to other IP subnets.

![Network second step](/img/User/network_form2.png)

Usually none of these settings are relevant for a basic network configuration.
After clicking on create the network is ready for use.
If you want to connect a running VM to a network go to Project -> Compute -> Instances. In the row the VM that should be connected to the network click on the arrow in the leftmost column and select "Attach Interface". In the following form select the network you want to connect to the network and click "Attach Interface". The VM is now connected to a VM.
It is also possible to connect a VM to a network on startup. In the Instances section click on "Launch Instance". In the Networks form select the network using the "+" button. One network is usually selected by default.
If you connect multiple machines to the same network they are connected to each other and can be accessed using their IP Adresses that are displayed in the Instances section in the IP Address Column from each other.
Although they are internally connected they can not see other networks. This includes other networks in the cloud as well as networks outside of the cloud like the internet.
It is also not possible to access any of the VMs from outside their own network.

### Connecting VMs in different networks

To access VMs in seperate networks a router is needed.
Routers are used to connect networks to each other so VMs in one network can access machines in the other network. To create a router go to Rpoject -> Network -> Routers and click on Create Router in the upper right corner. The following form as three fields:

*  Router Name: Name of the router

*  Admin State: Whether the network is up and forwarding packets

*  External Network: External network connected with the router
The relevant fields are Router name which can be chosen freely and External Network which is the external network connected to the Router. External Network can be left free if no external network should be used. Please mind that an external network is needed to access adresses outside the networks connected to the router like the internet. Currently two external networks are available:

*  external_network

*  biodb-net
Those two external networks serve different purposes. The external_network network is used to access internet. Biodb-net is a network that is used to access a NFS share with common biological databases in read only mode.

### Floating IPs

Floating IPs are used to make VMs publicly accessible from other networks, for example the internet. Floating IPs come from external networks. As described there are two external networks currently available in the cloud. The external_network and the biodb-net. To make a VM accessible from the Internet it is necessry to allocate a floating IP from the external_network. The problem in our cloud is that the number of available public IPs is very limited which means that each project is only allowed to allocate a single one. In well founded circumstances it is possible to get another IP. If you do fele the need to get another IP please contact the support. Please mind that at first the support will try to find a way to mitigate your problem without using more IPs. One pattern to avoid using multiple floating IPs is by using one VM as jump host. That VM has the credentials to ssh into all the other VMs.
