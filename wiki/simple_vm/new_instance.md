# Starting a virtual machine

To start a virtual machine, you need to belong to a SimpleVM project.
If you can't see the “New Instance” button in the sidebar on the left, you either need to reload the page,
or you don't belong to a SimpleVM project.

A message informs you if you can't start a virtual machine. This can happen if:

- You haven't enough resources:
    - Delete running virtual machines to free resources.
    - An administrator of your project can [request more resources](../portal/modification.md).
- Members of your project may not launch virtual machines:
    - Ask an administrator of your project to start a virtual machine for you.
    - Ask an administrator of your project to change the appropriate setting.

## Mandatory configuration

![overview_one](./img/new_instance/new_instance_overview_one.png)

### 1. Selected project

This select shows the selected project for which you want to start a new virtual machine and only shows when
you belong to more than one project.

### 2. Used and allocated resources

This line shows the resources used in your project and the resources available.

### 3. Name of your virtual machine

Name your virtual machine here or generate a random name. 
After starting your virtual machine, a unique ID appends to the name.

### 4. Flavor selection

Choose the flavor of your virtual machine.
Click on a tab to switch between flavor types or use the filter to search by name.
A flavor sets the resources of your virtual machine.<br>
See [here](../Concept/flavors.md) for more information about flavors.

#### About ephemeral flavors

Ephemeral flavors offer extra disk space. 
That extra disk space mounts to the virtual machine when it starts and offers faster access than a volume.<br>
Contrary to a volume, data on an ephemeral don't remain when you delete your virtual machine.
Data on an ephemeral remain when you reboot or pause your vm.
Further, snapshotting a vm doesn't persist data from an ephemeral.<br>
Therefore, you should use ephemeral storage for temporary data that often changes
(e.g. cache, buffers, or session data) or data often replicated across your environment.
If you need to persist data from an ephemeral, [create a backup on a volume](./backup.md).<br>
Use [block storage volumes](#volumes) for data that must persist.

???+ danger "Backup important data from an ephemeral"
    Ephemeral storage is a fleeting storage. 
    All data will be irretrievably lost when you delete your vm.
    If you need to persist any data from an ephemeral, [create a backup on a volume](./backup.md).

### 5. Image selection

Choose the image your virtual machine starts with.
An image includes the operating system and tool packages installed on your vm.<br>
You may choose between base images provided by de.NBI, pre-build images containing a Research Environment
provided by de.NBI, or one of your snapshots.
Click on a tab to switch between them or use the filter to search by name.<br>
For more information about images and snapshots, see [here](./snapshots.md).

## Optional configuration

### Volumes

Create, attach, and mount a new volume or attach and mount an already existing volume.<br>
If you want to know more about volumes, see [here](./volumes.md) page.

#### New volume

![vol_new](./img/new_instance/new_instance_vol_new.png)<br>
Name your volume.<br>
Input a mount path.
This is the absolute path where you may find the volume on your virtual machine.<br>
Choose the amount of storage.<br>
Either discard or add the volume to your vm configuration.

#### Attach existing volume

![vol_ex](./img/new_instance/new_instance_vol_ex.png)
Input a mount path.
This is the absolute path where you may find the volume on your virtual machine.<br>
Either discard or add the volume to your vm configuration.

#### Overview of your attached volumes

After adding a volume, you see an overview of the name, the mount path, and the storage in GB of your chosen volumes:
![vol_done](./img/new_instance/new_instance_vol_done.png)

### Conda tools

![conda](./img/new_instance/new_instance_conda.png)
You may choose conda, bioconda, and anaconda tools, which install on your machine at launch.
To add a tool, you may filter by name, and click the green plus button.<br>
For more information, see the [customization wiki page](./customization.md#conda).

### Browser-based Research environments

![resenv](./img/new_instance/new_instance_resenv_name.png)
Choose from a variety of browser-based research environments, respectively web IDEs, which install 
on your machine at launch.<br>
For more information, see the [customization wiki page](./customization.md#research-environments).

### Grant access for project members

![add_users](./img/new_instance/add_users_to_vm.png)
Grant members of your project SSH access to your virtual machine.<br>
You can't grant access to members without an SSH key stored in the portal.
The column “Public Key Set” displays whether they have an SSH key stored.
Find out how to set an SSH key [here](../portal/user_information.md#ssh-key).<br>
Each granted member can access your virtual machine with their respective private key.

???+ info "Granted members and permissions"
    All users connected to your vm have the same permissions and don't have separate home directories.<br>
    Only the person who initially started the machine can stop, restart, or delete it.

### Optional parameters

![optionals](./img/new_instance/new_instance_optional.png)

#### MOSH / UDP ports

You may open UDP ports and have `MOSH` installed on your virtual machine.
Open UDP ports offer better mobile usage when using `MOSH`.<br>
For more information on UDP ports and MOSH, see the [MOSH wiki page](../Tutorials/Mosh/index.md).

## Start VM

Read and confirm some acknowledgments and start your virtual machine.<br>
After a short time, the page redirects you to the [Instance Overview](./instance_overview.md) page.
