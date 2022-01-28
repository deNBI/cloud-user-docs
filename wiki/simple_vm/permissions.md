# Group Permissions

There are two roles within a project: **admins** and **non-admins**.<br> 
Especially for SimpleVM projects, these roles play an expanded role in resource usage authorization.<br> <br> 
An **admin** generally has all rights, not limited to own resources (like vms).  
**Non-admins** are generally only allowed to modify their own resources - unless they have been explicitly granted access.  
SimpleVM project admins are able to prevent the starting of machines by non-admins in their projects.  
Workshop participants which are not admins are not allowed to start machines by default. 
The permission of starting machines by non-administrators can be changed in the project overview.  
Workshops can only be interacted with by admins.  
<br> <br> The following table illustrates the different rights:

| Type                 | Project              |                       |                      |                      |
|----------------------|----------------------|-----------------------|----------------------|----------------------|
|                      | Admin                |                       | Member               |                      |
| **VM**               | Own                  | Others                | Own                  | Others               |
| Create               | :material-check-all: | :material-check: ^1^  | :material-check: ^2^ | :material-check: ^1^ |
| List                 | :material-check-all: | :material-check-all:  | :material-check-all: | :material-close:     |
| Stop/Restart         | :material-check-all: | :material-check-all:  | :material-check-all: | :material-close:     |
| Reboot (Hard & Soft) | :material-check-all: | :material-check-all:  | :material-check-all: | :material-close:     |
| View Details         | :material-check-all: | :material-check-all:  | :material-check-all: | :material-close:     |
| Create Snapshot      | :material-check-all: | :material-check-all:  | :material-check-all: | :material-close:     |
| Attach Volume        | :material-check-all: | :material-check-all:  | :material-check-all: | :material-check:     |
| Detach Volume        | :material-check-all: | :material-check-all:  | :material-check-all: | :material-check: ^3^ |
| Connect              | :material-check-all: | :material-check-all:  | :material-check-all: | :material-check: ^4^ |
| Delete               | :material-check-all: | :material-check-all:  | :material-check-all: | :material-close:     |
| Create Snapshot      | :material-check-all: | :material-check-all:  | :material-check-all: | :material-close:     |
| **Snapshot**         | Own                  | Others                | Own                  | Others               |
| List                 | :material-check-all: | :material-check-all:  | :material-check-all: | :material-check-all: |
| Use                  | :material-check-all: | :material-check-all:  | :material-check-all: | :material-check-all: |
| Delete               | :material-check-all: | :material-check-all:  | :material-check-all: | :material-close:     |
| **Volumes**          | Own                  | Others                | Own                  | Others               |
| Create               | :material-check-all: | :material-close:      | :material-check-all: | :material-close:     |
| List                 | :material-check-all: | :material-check-all:  | :material-check-all: | :material-check-all: |
| Delete               | :material-check-all: | :material-check-all:  | :material-check-all: | :material-close:     |
| Rename               | :material-check-all: | :material-check-all:  | :material-check-all: | :material-close:     |
| Allowed to attach    | :material-check-all: | :material-check-all:  | :material-check-all: | :material-check-all: |
| Extend               | :material-check-all: | :material-check-all:  | :material-check-all: | :material-close:     |
| **Cluster**          | Own                  | Others                | Own                  | Others               |
| Create               | :material-check-all: | :material-check: ^1^  | :material-check: ^2^ | :material-check: ^1^ |
| List                 | :material-check-all: | :material-check-all:  | :material-check-all: | :material-close:     |
| Scale (Up & Down)    | :material-check-all: | :material-check-all:  | :material-check-all: | :material-close:     |
| Delete               | :material-check-all: | :material-check-all:  | :material-check-all: | :material-close:     |
| **Workshop**         | Own                  | Others                | Own                  | Others               |
| Create               | :material-check-all: | :material-check-all:  | :material-close:     | :material-close:     |
| List                 | :material-check-all: | :material-check-all:  | :material-close:     | :material-close:     |
| Delete               | :material-check-all: | :material-check-all:  | :material-close:     | :material-close:     |

<br>

^1^: Admins of workshop projects are able to start machines for members of their workshop project. 
Also admins and project members are able to start machines and cluster and grant access for other project members.  
^2^: The starting of machines by non-admin project members can be prevented by project admins.  
^3^: A volume can be detached from any machines by the owner of the volume.  
^4^: The connection to a machine is only possible if the owner of the machine has granted access to the respective user. 
This can also be achieved by adding the respective users public key to the virtual machine manually.
