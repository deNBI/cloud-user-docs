# Cluster

## General Information

In addition to single machines, SimpleVM users are also able to start entire clusters. The cluster feature is currently still in the development phase, which is why the corresponding SimpleVM project must be activated in order to use it. 

Our cluster feature enables the orchestration of several virtual machines in order to distribute the tasks to individual instances. In our system, we distinguish between the master instance and the worker nodes. The flavour of the individual nodes and the flavour of the master instance can differ, only the image is the same for all instances. 
The instances are connected to each other and can thus exchange data. 

In SimpleVM, it is possible to expand the clusters with additional machines depending on the resources required, or to remove nodes that are no longer needed from the cluster - we call this up- and down-scaling. The instructions for this procedure can be found on the [wiki page](./cluster_overview.md#3-scale-up) of the instance overview.


## Shared directories

Local disk space of the master node is provided as a shared spool-disk space between master and all workers.
It can be found at the path `/vol/spool`. 
`/vol/scratch/` corresponds to the path of the ephemeral disk, thus the local disk space of a single node or a master node.

## Starting and managing of clusters


In SimpleVM, clusters can be used very similarly to normal instances. Starting can be initiated via the 'New Cluster' page, which is structured analogously to the 'New Instance' page. To do this, [look here](./new_cluster.md).


The management or checking of running clusters also works analogously to the instance overview. The cluster overview is described in more detail [here](./cluster_overview.md).


## BiBiGrid

When you are an OpenStack user, there is a [tutorial](../../Tutorials/BiBiGrid/index.md) on how to use [BiBiGrid](https://github.com/BiBiServ/bibigrid).

