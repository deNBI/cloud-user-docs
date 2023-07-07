# Portal

The de.NBI Cloud portal represents the central access point to the de.NBI Cloud.

## Principal Investigator
A Principal Investigator (PI) is a person who is responsible for the design, conduct, and overall management of a research project. The PI is typically the lead researcher on a project and is responsible for overseeing a team of scientists, technicians, and other personnel who are involved in the project. The PI is responsible for developing the research plan, securing funding for the project, and ensuring that the project is completed on time and within budget.

In academia, the PI is often a professor or other senior researcher who has been awarded a grant or contract to conduct the research. In industry, the PI may be a scientist or engineer who is employed by a company and is responsible for leading research and development projects.

In both academic and industrial settings, the PI plays a key role in determining the direction and outcome of a research project and is often the main point of contact for funding agencies, collaborators, and other stakeholders.
## Project Application

An application for resources in the de.NBI Cloud can be submitted by any team member, but must be verified by a principal investigator of a German university or research institution.
After you submitted the application, you will receive a confirmation mail. Your application will be reviewed by a scientific committee.
You will be notified as soon as possible whether your application is approved or declined. 

You can submit an application by login to the [de.NBI Cloud portal](https://cloud.denbi.de/portal/) and selecting the "New application" tab (see below).

![Project Application Tab](img/project_application_tab.png)

Besides general project information like project name, project description, institution name and project lifetime, you also have to provide the information
independing on the project type you choose:
 
 * The **Simple VM** Project type allows you to start virtual machines without configuring a project in OpenStack (e.g. network configuration). 

 * In a **Cloud Project**  you will have your own OpenStack project and you are free to configure your network, virtual machines and storage setup.
 
### Application Status

The review of your application follows a series of different stages. The progress is visible in the [project overview](project_overview.md).

### Requesting Resources

#### General Information regarding requested resources

In addition to the general information of the project, the required resources must be indicated in the application.
This concerns several relevant parameters in cloud computing. 
Please keep in mind: The resources requested and approved in the project application are not definite. They can be modified in the current project by change requests.

### Terms

The following is a list of important terms with explanations:

#### Flavor

When applying for a project, flavors must be selected. 
A single flavor describes the base resources available for a single VM. 
A flavor specifies the available number of VCPUs, the amount of RAM and disk space for a single VM started of that type. 
If available, it also specifies the space that is provided on an ephemeral disk.
GPU flavors provide graphics cards connected to the VM.

#### VCPU
A VCPU, short for Virtual Central Processing Unit, is a virtualized representation of a physical CPU that enables the concurrent operation of multiple virtual machines on a single physical server.
It facilitates the efficient utilization of computing resources and enhances the sharing of processing power in virtualization and cloud computing environments.

#### RAM
RAM stands for "Random Access Memory." It is a type of computer memory that is used for temporary data storage and quick access by the computer's processor. RAM stores data that is actively being used by running programs and allows for fast read and write operations.

#### Hard Disk

A hard disk, also known as a hard drive or HDD (Hard Disk Drive), is a storage device used in computers to store and retrieve digital data.

#### Ephemeral Disk
An ephemeral disk is a temporary storage disk provided to a virtual machine (VM) in cloud computing environments. Unlike a persistent disk or a hard disk drive, ephemeral disks are not intended for long-term storage or data persistence.

#### GPU
GPU stands for "Graphics Processing Unit." It is a specialized electronic circuit or chip designed to handle and accelerate graphics rendering and image processing tasks in a computer system.

#### Storage and Volumes

Both a number of storage volumes and an amount of required disk space can be specified. The specified storage space can be divided as desired among the available volumes.
The purpose of volumes is to persist data so that it is available, for example, even after a VM has been deleted.
For OpenStack projects, object storage is also available. Object storage is a type of storage to store and share data in cloud environments.

### Cloud Project

For a **Cloud Project** you have to specify the following parameters:

* Number of Virtual Machines

* Cores per VM

* Disk per VM

* RAM per VM

* Object Storage

* Special Hardware (GPU/FPGA)
