# Portal

The de.NBI Cloud portal represents the central access point to the de.NBI Cloud.

## Allocation

An application for resources in the de.NBI Cloud must be submitted by a principal investigator of a german university or research facility.
After you submitted the application, you will receive a confirmation mail. Your application will be reviewed by a scientific committee.
You will be notified as soon as possible whether your application is approved or declined. 

You can submit an application by login to the [de.NBI Cloud portal](https://cloud.denbi.de/portal/) and selecting the "New application" tab (see below).

![Project Application Tab](img/project_application_tab.png)

Besides general project information like project name, project description, institution name and project lifetime, you also have to provide the information
independing on the project type you choose:
 
 * The **Single VM** Project type allows you to start virtual machines without configuring a project in OpenStack (e.g. network configuration). 

 * In a **Cloud Project**  you will have your own OpenStack project and you are free to configure your network, virtual machines and storage setup.

### Single VM

In a **Single VM** project you just have to provide the number of virtual machines you would like to run in parallel in your project.
Once your application is approved you can choose between the following flavors for every virtual machine:

* de.NBI Large (CPUs:32, RAM:64 GB)

* de.NBI.large+ephemeral (CPUs: 32, RAM: 64GB, Disk: 250 GB)

* de.NBI Medium (CPUs:16, RAM:32 GB, Disk: 50 GB)

* de.NBI.medium+ephemeral (CPUs: 16, RAM: 32 GB, Disk: 150 GB)

* de.NBI Small (CPUs:8, RAM:16 GB)

* de.NBI.small+ephemeral (CPUs: 8, RAM: 16 GB, Disk: 50 GB)

### Cloud Project

For a **Cloud Project** you have to specify the following parameters:

* Number of Virtual Machines

* Cores per VM

* Disk per VM

* RAM per VM

* Object Storage

* Special Hardware (GPU/FPGA)

## Project Overview

In the Project Overview tab you get a list of all your projects with details:

![Project Overview Tab](img/overview_tab.png)
![Project Overview](img/overview.png)


If a project is written in black text your lifetime limit isnt reached.

If a project is written in red text your lifetime limit has been exceeded.

Actions are only visible to an admin

The following actions are possible:

* Show Members: shows all members of this project
    - admins are written in blue text
    - members are written in black text
    
![Members](img/members.png)

If you are an admin you can:

    - appoint another member to admin.
    - remove admin state.
    - remove a member from this project.
    
* Add Member: add another user to this project
    -  add a new user to the project by inserting first and/or lastname and pressing add member.
   
![Members](img/add_members.png)




#### Citation Information
The development and support of the cloud is possible above all through the funding of the cloud infrastructure by the Federal Ministry of Education and Research (BMBF)! We would highly appreciate the following citation in your next publication(s):

!!! note "" 
    ‘This work was supported by the BMBF-funded de.NBI Cloud within the German Network for Bioinformatics Infrastructure (de.NBI) (031A537B, 031A533A, 031A538A, 031A533B, 031A535A, 031A537C, 031A534A, 031A532B).  
