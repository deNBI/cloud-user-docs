# Volumes in the de.NBI Cloud

*Volumes* are durable data storage devices which can be attached to virtual machines (VM). Just like for example portable hard drives they can only be attached to one VM at the same time. Nevertheless, volumes can be attached, detached and reattached as often as desired. Thus, volumes can be used to persistently store data and transfer it between different VMs.


### Creating volumes in the cloud

In the Horizon web interface (OpenStack Dashboard) click on **Volumes** and then on **Create Volume**:

![volumes overview](/img/User/volumes.png)

In the new popup, provide a name, a description, a type and the size of the new volume:

![creating volumes](/img/User/create_volume.png)

_The available types may vary between the de.NBI cloud sites!_

After clicking the *Create Volume* button OpenStack immediately starts to create a new volume which then can be attached to a virtual machine.

### Snapshots

*Snapshots* are copies of attached or detached volumes. Hereby, the current state of a volume gets persisted, i.e. all its data. This can be used to (periodically) create backups of data volumes or to duplicate certain volumes containing for example databases or software.
