# Cluster

## General Information

In addition to single machines, SimpleVM users are also able to start entire clusters. The cluster feature is currently still in the development phase, which is why the corresponding SimpleVM project must be activated in order to use it. 

## Shared directories

Local disk space of the master node is provided as a shared spool-disk space between master and all workers.
It can be found in the path `(/vol/spool)`. 
`/vol/scratch/` corresponds to the path of the ephemeral disk, thus the local disk space of a single node or a master node.

## Starting and managing of clusters


In SimpleVM, clusters can be used very similarly to normal instances. Starting can be initiated via the 'New Cluster' page, which is structured analogously to the 'New Instance' page. To do this, [look here](./new_cluster.md).


The management or checking of running clusters also works analogously to the instance overview. The cluster overview is described in more detail [here](./cluster_overview.md).


