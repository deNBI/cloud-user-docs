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

### Simple VM

In a **Simple VM** project you just have to provide the number of virtual machines you would like to run in parallel in your project.
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

#### Citation Information
The development and support of the cloud is possible above all through the funding of the cloud infrastructure by the Federal Ministry of Education and Research (BMBF)! We would highly appreciate the following citation in your next publication(s):

!!! note "" 
    ‘This work was supported by the BMBF-funded de.NBI Cloud within the German Network for Bioinformatics Infrastructure (de.NBI) (031A537B, 031A533A, 031A538A, 031A533B, 031A535A, 031A537C, 031A534A, 031A532B).  

## Simple VM Project

### Images

#### X2Go Image

You can start an X2Go image when you select an image starting with the X2Go label e.g `X2Go_xfce`.
Once your image started,yYou will see a message similiar to the following one:

![X2Go Command](img/x2go_command.png)

Provide the data in the red rectangle in the settings of your x2go client:

![X2Go Client](img/x2go_client.png)

You also have to select the session type and the private key of your public ssh key that you provided in the user information tab. 
Please select also theelect the session 
