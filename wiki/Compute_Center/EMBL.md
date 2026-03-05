# de.NBI cloud at EMBL

EMBL currently runs a Kubernetes cluster based on Rocky Linux 9 and Kubespray. You can find information about [Kubespray](https://github.com/kubernetes-sigs/kubespray) on github but it is mostly a plain Kubernetes installation. General Documentation can be found [at the official Kuberentes Docuementation page](https://kubernetes.io/docs/home/) We also use Capsule for multi-tenancy. More information about Capsule can be found [on their github page](https://projectcapsule.dev/) It allows us to easily separate projects and users.

## Contact

The de.NBI cloud team at EMBL can be contacted via denbi-requests(at)embl.de

## Login

Currently we restrict access to our Kubernetes cluster via OIDC connected to our in house Keycloak installation. Once a project has been accepted you will be given Credentials to our DeNBI domain. We use Apache Guacamole to allow web based access to the cluster. [Login](https://bastion-prod(dot)denbi(dot)cloud(dot)embl(dot)de)

## Network

EMBL de.NBI Kubernetes cloud is separated into a DMZ network with limited access to other networks. A pool of IPV4 public IPs are available on request. You will be able to set up internet facing services at ports of your choice (with a few exceptions). It should be possible to create [Kubernetes Services](https://kubernetes.io/docs/concepts/services-networking/service/) of type LoadBalancer to get a public ip.
We're not providing DNS services but you're welcome to come up with your own DNS arrangemets for services you set up.

## Object storage

EMBL instance offers some object storage for testing. We currently use on premise minio.

## Protection against loss of data

Be advised that stateless services are expected in Kubernetes and stateful services require extra setup. We offer NFS storage via Kubernetes CSI based storage Classes via [Netapp Trident](https://www.netapp.com/trident/). Be advised that this is not a backup. If you want true backups, independent of this cloud-center, you have to copy your data to a safe location, like an external harddrive, yourself. We do our best to prevent any data loss, but
we can't guarantee that 100%.

## Kubernetes documentation

As we run a fairly vanilla Kubernetes installation most of the documentation available online should be applicable. We have internal example of deployments and services available on request. We also have a number of Custom resource definitions in our cluster like Database CRDs for MariaDB, MongoDB and PostgreSQL.

## Flavors

Differntly to Openstack Flavours Kubernetes pods can be provisioned with a specific resources via Yaml in their deployments.

``` yaml
   resources:
      requests:
        memory: "64Mi"
        cpu: "250m"
      limits:
        memory: "128Mi"
        cpu: "500m"

```

It is also possible to deploy containers with access to Nvidia GPUs via the NVIDIA operator in Kubernetes.

```yaml
   resources:
      requests:
        memory: "64Mi"
        cpu: "250m"
        nvidia.com/gpu: 1
      limits:
        memory: "128Mi"
        cpu: "500m"
        nvidia.com/gpu: 1


```

## Happy computing
