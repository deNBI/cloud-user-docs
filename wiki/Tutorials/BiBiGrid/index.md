# Setup BiBiGrid (Workshop 8.3.2018)

### Prerequisites

- Java 8/9
- Openstack API access
- git & maven 3.3 (or better) to build bibigrid from sources

## Build from sources

- Clone GitHub repository `https://github.com/bibiserv/bibigrid`
- Change into project dir `cd bibigrid`
- Switch to development branch `git checkout development`
- build Java executable for Openstack `mvn -P openstack clean package`
- Call `java -jar bibigrid-main/target/bibigrid-openstack-2.0.jar -h` to get help messages and check if executable works


## Download Binary

If you don't want build the client from sources you can use a prebuilt binary. 
[BiBiGrid Openstack Java executable](http://bibiserv.cebitec.uni-bielefeld.de/resources/bibigrid/bibigrid-openstack-2.0.jar)


# Getting started

Check the [GitHub repository](https://github.com/BiBiServ/bibigrid/tree/development) for detailed information about BiBiGrid. Be sure that you are on the development branch.

## Configuration

The goal of this session is to setup a small HPC cluster consisting of 5 nodes  (1 master, 4 slaves)  using BiBiGrid. The template below do the job, you have to replace all XXX's. 

### Template

```
#use openstack
mode: openstack

openstackCredentials:
  username: XXX
  tenantName: XXX
  domain: elixir
  tenantDomain: elixir
  endpoint: https://openstack.cebitec.uni-bielefeld.de:5000/v3/
  password: XXX


#Access
identityFile: XXX
sshUser: ubuntu
keypair: XXX
region: Bielefeld
availabilityZone: default

#Network
subnet: XXX

#BiBiGrid-Master
masterInstance:
  type: unibi.micro
  image: febceb9a-fb0f-4f1c-ad06-8caf6340de64

#BiBiGrid-Slave
slaveInstances:
  - type: unibi.micro
    count: 4
    image: febceb9a-fb0f-4f1c-ad06-8caf6340de64

#Firewall/Security Group
ports:
  - type: TCP
    number: 80

#services
nfs: yes
oge: yes
cloud9: yes

```

## Start the Cluster

`java -jar bibigrid-main/target/bibigrid-openstack-2.0.jar -c`

or more verbose:

`java -jar bibigrid-main/target/bibigrid-openstack-2.0.jar -c -v`

Starting with blank Ubuntu 16.04 images takes up to 20 minutes to finish.
Using preinstalled images is much faster (about 5 minutes).


## Login into the Cluster

After a successful setup you can login into the master node. Run `qhost` 
to check if there are 4 execution nodes available.


### Cloud9

Cloud9 is Web IDE that allows a more comfortable way to work with your cloud instances. Although cloud9 is an alpha state, it is stable enough to use for an environment like ours. Let's see how this works together with BiBiGrid. 
For security reasons cloud9 is not started during startup. We need a valid certificate and some kind of authentication to create a safe connection, which is not that easy in a dynamic cloud environment. 

However, we use ssh to tunnel the default cloud9 port (8181)  to our local machine and start cloud9 listening only on localhost.


1. create ssh tunnel : `ssh -L 8181:localhost:8181 129.70.51.20`.

2. start cloud9 listening at localhost and using `~/playbook` as workspace: `cloud9 --listen localhost -w ~/playbook`

3. cloud9 IDE is then available at `http://localhost:8181`

4. at first start, cloud9 needs to install some additional software, follow the instructions




## List running cluster


## Terminate a cluster
