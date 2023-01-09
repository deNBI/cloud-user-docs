# Instance overview

On the “Instance Overview” you can list virtual machines, get more information, and manage them.

![layout](./img/instance_overview/instance_overview_general.png)

## 1. Pagination

Set how many VMs you want to see on a page and scroll through the pages.

## 2. Filter

Filter the list of VMs:

- By username
- By project name
- By a users Elixir ID
- By an OpenStack VM ID
- By vm name
- By flavor name

Click `Filter`.

## 3. Action on many machines

Trigger an action on all selected virtual machines.<br>
`Select all` or `select` specific machines.

## 4. General information

See the name, the status, the project, and the creator of the virtual machine.<br>
Click on the name to get to the [Detail page](instance_detail.md). Click on the project name to get
to the [Project overview](../portal/project_overview.md).

## 5. Descriptive icons

Get a quick overview of the configuration:  

* See the amount of volumes mounted to the vm.
* See the installed research environment and whether it installed correctly.<br>
  Hover to read the name.<br>
  Click the icon to copy the URL of your browser-based research environment.
* See the amount of conda tools installed on the virtual machine at launch and whether they installed correctly.

## 6. Flavor and Image

Which flavor and image the virtual machine runs on.

## 7. Virtual machine detail page

Go to the virtual machine [detail page](instance_detail.md).

## 8. How to connect

Get commands and information on how to connect to your virtual machine.

![htc](./img/instance_overview/instance_overview_htc.png)  

1. The commands you find here differ depending on the chosen configuration.  
2. Click to copy only the command, not the descriptive text.

## 9. Action on one machine

Perform actions on the machine.<br>
Depending on the status, you only see a selection of actions.

![actions](./img/instance_overview/instance_overview_actions.png)  

###### Attach Volume

Attach an existing volume. This action shows when the machine is active and running.

###### Detach Volume

Detach an attached volume. This action shows when the machine is active and running.

###### Stop VM

Shutoff the virtual machine.

???+ info "Resource usage"
    A vm in “SHUTOFF” state still consumes resources.

###### Reboot VM

Soft or hard reboot the virtual machine.<br>
A soft reboot attempts a graceful shut-down and restart of the instance. 
A hard reboot power cycles the instance.[^1]  

###### Create snapshot

Take a snapshot of the virtual machine.<br>
You, or a project member, can boot a new virtual machine from it. 
For more information on snapshots, see [here](./snapshots.md).

###### Delete VM

Delete the virtual machine.<br>
Any attached volume gets detached and not deleted.

???+ warning "Backup your data"
    All data on the machine gets deleted. Make sure to back up data you can't lose. 
    See [here](backup.md) for backup recommendations.

###### Resume/Restart VM

Boot up the "SHUTOFF" virtual machine.

[^1]: https://docs.openstack.org/mitaka/user-guide/cli_reboot_an_instance.html
