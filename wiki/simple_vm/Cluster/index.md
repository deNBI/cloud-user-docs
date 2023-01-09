# Cluster

Besides single machines, SimpleVM users can start entire clusters.
Since the cluster feature is still in the development phase,
only selected projects can use it.
Contact [cloud-helpdesk@denbi.de](mailto:cloud-helpdesk@denbi.de) if you want the cluster feature
activated for your project.

The cluster feature enables the orchestration of several virtual machines to distribute tasks to instances.
It distinguishes between a master instance and worker nodes. 
The flavor of each node and the flavor of the master instance can differ. 
Only the image is the same for all instances. 
The instances are connected to each other and can thus exchange data.
<br>
<br>
In SimpleVM, you can add worker nodes to your cluster, called **up scaling**.
You can remove worker nodes from your cluster, called **down scaling**.
See the instructions [here](./cluster_overview.md#3-scale-up).

## Shared directories

The master node provides shared spool-disk space between the master and all worker nodes.
You can find it under the path `/vol/spool`.<br>
`/vol/scratch/` corresponds to the path of the ephemeral disk, thus the local disk space of a single worker node or a 
master node.

## Start and manage your clusters

In SimpleVM, you use clusters similarly to your usual virtual machines.
Start a cluster on the "New Cluster" page and manage your cluster on the "Cluster overview".
See [New Cluster](new_cluster.md) for information on starting a cluster, 
see [Cluster Overview](cluster_overview.md) for information
about the cluster overview.

## OpenStack and BiBiGrid

If you belong to an OpenStack project, see this [BiBiGrid tutorial](../../Tutorials/BiBiGrid/index.md) on how
to use [BiBiGrid](https://github.com/BiBiServ/bibigrid).
SimpleVM uses BiBiGrid to offer the cluster feature.
