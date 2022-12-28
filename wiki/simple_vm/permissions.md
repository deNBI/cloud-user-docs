# Group Permissions

Each project member can have one of the following roles within a project: **administrator** or **member**.
In SimpleVM projects, each role has different permissions.
<br>
<br>
An **administrator** has the most permissions, not limited to their own resources, like virtual machines, volumes,
or snapshots. They can prevent **members** from creating new virtual machines and toggle this setting in the
project overview. They can interact with workshops.
<br>
<br>
A **member** has the fewest permissions, limited to their own resources, like virtual machines, volumes, or snapshots.
**Administrators** and others must grant access to their resources first.
Workshop participants with the **member** role have no permission to create new virtual machines by default.
<br>
<br>
The following table illustrates the permissions:

|          Method          |         Role         |                       |                       |                       |
|:------------------------:|:--------------------:|:---------------------:|:---------------------:|:---------------------:|
|                          |        Admin         |                       |        Member         |                       |
|          **VM**          |       Own[^1]        |      Others[^2]       |        Own[^1]        |      Others[^2]       |
|         `Create`         | :material-check-all: | :material-check: [^3] | :material-check: [^4] |   :material-close:    |
|         `Access`         | :material-check-all: | :material-check: [^7] | :material-check-all:  | :material-check: [^7] |
|          `List`          | :material-check-all: | :material-check-all:  | :material-check-all:  |   :material-close:    |
|      `Stop/Restart`      | :material-check-all: | :material-check-all:  | :material-check-all:  |   :material-close:    |
|  `Reboot (Hard & Soft)`  | :material-check-all: | :material-check-all:  | :material-check-all:  |   :material-close:    |
|      `View Details`      | :material-check-all: | :material-check-all:  | :material-check-all:  |   :material-close:    |
|    `Create Snapshot`     | :material-check-all: | :material-check-all:  | :material-check-all:  |   :material-close:    |
|     `Attach Volume`      | :material-check-all: | :material-check-all:  | :material-check-all:  |   :material-check:    |
|     `Detach Volume`      | :material-check-all: | :material-check-all:  | :material-check-all:  | :material-check: [^5] |
|         `Delete`         | :material-check-all: | :material-check-all:  | :material-check-all:  |   :material-close:    |
|    `Create Snapshot`     | :material-check-all: | :material-check-all:  | :material-check-all:  |   :material-close:    |
|       **Snapshot**       |         Own          |        Others         |          Own          |        Others         |
|          `List`          | :material-check-all: | :material-check-all:  | :material-check-all:  | :material-check-all:  |
|          `Use`           | :material-check-all: | :material-check-all:  | :material-check-all:  | :material-check-all:  |
|         `Delete`         | :material-check-all: | :material-check-all:  | :material-check-all:  |   :material-close:    |
|       **Volumes**        |         Own          |        Others         |          Own          |        Others         |
|         `Create`         | :material-check-all: |   :material-close:    | :material-check-all:  |   :material-close:    |
|          `List`          | :material-check-all: | :material-check-all:  | :material-check-all:  | :material-check-all:  |
|         `Delete`         | :material-check-all: | :material-check-all:  | :material-check-all:  |   :material-close:    |
|         `Rename`         | :material-check-all: | :material-check-all:  | :material-check-all:  |   :material-close:    |
|   `Allowed to attach`    | :material-check-all: | :material-check-all:  | :material-check-all:  | :material-check-all:  |
|         `Extend`         | :material-check-all: | :material-check-all:  | :material-check-all:  |   :material-close:    |
|       **Cluster**        |         Own          |        Others         |          Own          |        Others         |
|         `Create`         | :material-check-all: |   :material-close:    | :material-check: [^4] |   :material-close:    |
|          `List`          | :material-check-all: | :material-check-all:  | :material-check-all:  |   :material-close:    |
|   `Scale (Up & Down)`    | :material-check-all: | :material-check-all:  | :material-check-all:  |   :material-close:    |
|         `Delete`         | :material-check-all: | :material-check-all:  | :material-check-all:  |   :material-close:    |
|       **Workshop**       |         Own          |        Others         |          Own          |        Others         |
|         `Create`         | :material-check-all: | :material-check-all:  |   :material-close:    |   :material-close:    |
|          `List`          | :material-check-all: | :material-check-all:  |   :material-close:    |   :material-close:    |
|         `Delete`         | :material-check-all: | :material-check-all:  |   :material-close:    |   :material-close:    |
| **Research environment** |         Own          |        Others         |          Own          |        Others         |
|         `Access`         | :material-check-all: | :material-check:[^6]  | :material-check-all:  | :material-check:[^6]  |

<br>

[^1]:
    For or from own, depending on the context.
[^2]:
    For or from others, depending on the context.
[^3]:
    Administrators of workshop projects can start virtual machines for members of their workshop project. 
[^4]:
    Administrators can prevent members from starting virtual machines.   
[^5]:
    A volume owner can detach their volume from every machine.
[^6]:
    Owner must grant access first.<br>
    Administrators of workshops have access permission by default.
[^7]:
    When creating a virtual machine, you can grant others access to your virtual machine.<br>
    After creating, you can grant access by placing their public key onto your virtual machine.
