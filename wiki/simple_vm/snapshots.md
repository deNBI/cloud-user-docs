# Images and snapshots

You use an image, or a snapshot, to boot your virtual machine.

## Image

Images contain a bootable operating system, for example, a Linux derivative as Ubuntu or CentOS.
They can have further collections of tools, packages, and configurations, for example RStudio or Apache Guacamole.<br>
While each cloud site provides a selection of images you can use to boot up a virtual machine,
de.NBI provides the same selection of images for every cloud site.

## Snapshot

A snapshot is an exact copy of your virtual machine.
You use the snapshot of an instance as the basis for another instance.<br>
A typical workflow can be:

- To create a virtual machine based on a de.NBI provided image, to configure
  the virtual machine with needed tools and packages, and to create a snapshot from that configuration.
  Afterward, you launch new virtual machines based on the snapshot, so that you don't need to configure
  it every time.
- To configure a virtual machine for a workshop, create a snapshot of that machine, and afterward, launch a virtual 
  machine for every user based on that snapshot.
- Save your configuration and data on your root disk to continue your work later.

???+ info "Snapshot limitation"
    A snapshot preserves the full state of RAM. Therefore, you can only snapshot a virtual machine with up to a 
    maximum of 256 GB RAM.


### Create a snapshot

After starting a machine you can go to the [instance overview](instance_overview.md#9-action-on-one-machine) tab 
and create a snapshot, or you create one on the [detail page](instance_detail.md#general-information).
A window opens where you can enter a name for your snapshot. Confirm to create a snapshot.

![create snapshot](./img/snapshots/create_snapshot.png)

???+ danger "Don't create a snapshot of a running instance"
    Creating a snapshot of a running instance can lead to inconsistencies, lost data and a non-functioning and
    unrecoverable snapshot. 
    Stop your instance before creating a snapshot.

### View snapshots

![overview](./img/snapshots/overview.png)  

1. Set how many snapshots you want to see on a page and scroll through the pages.
2. Filter your list of snapshots. Filter by name, project name and the OpenStack ID of the snapshot.
3. Perform an action on all selected snapshots. 'Select all' to select all snapshots or `select` specific snapshots.
4. Information about your snapshot: the name of the snapshot, the project name, and the status.
5. Delete the snapshot.

### Boot from a snapshot

After you successfully created the snapshot, you can go to the [new instance](./new_instance.md#5-image-selection) 
tab and choose your created snapshot as an image to start a vm. 

![start_vm_from_snap](./img/snapshots/startsnap.png)
