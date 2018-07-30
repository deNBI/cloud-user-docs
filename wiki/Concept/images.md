# Using and managing images

## Introduction
To start a virtual machine in OpenStack, a virtual machine image (brief: image) is required. Images are files that contain a bootable operating system. Cloud images are available for various operating systems like Ubuntu or CentOS. They are usually separated from the normal installation images. 
A various list of cloud-images can be found here:

* [Ubuntu Cloud Images](https://cloud-images.ubuntu.com/)
* [CentOS Cloud Images](https://cloud.centos.org/centos/7/images/)
* [Fedora Cloud Images](https://alt.fedoraproject.org/cloud/)
* [Windows Cloud Images](https://cloudbase.it/windows-cloud-images/)
 
Please keep in mind, that our OpenStack installation provides default and pre-configured images that are ready to use.

## Adding images to Openstack

To add an image to Openstack open the Openstack dashboard, go to Compute and then Images. In the upper right corner click "Create Image".
![Glance image overview](/img/User/images_overview.png)

 Fill in the fields in the opened form. For information to single fields, please refer to the following list. All fields not mentioned here are neither required by Openstack nor suggested to be used by normal users.

*  **Image Name**: Name of the image that is displayed in the image list. Please use a self describing name (e.g. Ubuntu_17.04).

*  **Image Description (optional)**: Description of the image. Could contain, for example, use cases.

*  **File**: Image file of the image that will be uploaded from the local file system.

*  **Format**: Format of the uploaded image file. For details on file formats please refer to the Image file format section.

*  **Minimum Disk**: Minimal amount of disk space required for the image to run. Will restrict the flavors that the image can be run on.

*  **Minimum RAM**: Same as Minimum Disk, bur for RAM. Also restricts the applicable flavors.

*  **Visibility**: Whether the image is publicly available or not. Please only use private images, although the default might be different. Usually regular users are not able to create public images.

*  **Protected**: Protects the image from unintended deletion.

![Create Image](/img/User/create_image.png)

The metadata can be left empty. For a more detailed documentation, please refer to the official documentation: [OpenStack image documentation](https://docs.openstack.org/image-guide/introduction.html).
To finish image creation, please click on "Create Image".
After a while, the image should now be visible in the Images list.

## Image file format

Image files come in different formats. Openstack supports a wide variety of image file formats.
The most common formats for images are QCOW2 and RAW. Please beware that files in iso format usually do not work as they are often used for regular OS installation and not prepared for cloud environments. For further informations please refer to the [Openstack image documentation](https://docs.openstack.org/image-guide/introduction.html).


## Image Management

All uploaded Images can be seen under Project -> Compute -> Images. Images can be created and deleted here.
![Images Overview](/img/User/images_overview.png)

In addition, it is also possible to launch instances with a specific image. Optionally you can boot from an existing volume.

## Images on volumes and ephemeral disks

When creating a virtual machine, the machine can either be created on an ephemeral disk using local storage or a volume. The size of the ephemeral disk is determined by the used flavor and the size of the volume chosen by the user. The decision of whether to use ephemeral storage or a volume for the VM can be made in the "Launch Instance" dialog in the Source section.
![Images Volume Boot](/img/User/images_volumeboot.png) 
If no new volume is created on startup, the ephemeral disk will be used. Otherwise, only the volume is used and there will be no ephemeral disk for this instance. When using a volume disk, Openstack currently does not check if the volume has sufficient space for the image but it still checks if the selected flavor has a sufficient amount of ephemeral disk space although the ephemeral disk is not used.

## Images and Flavors

When creating a VM, the user has to select a flavor. This flavor defines the resources a virtual machines has. There are various flavors predefined in Openstack. They vary in the number of available vCPUs, RAM and their disk setup.

*  vCPU: Number of CPUs available in the VM.

*  RAM: Amount of RAM available in the VM.

*  Total Disk: Amount of disk space available on root disk and ephemeral disk.

*  Root Disk: Root disk space.

*  Ephemeral Disk: Ephemeral disk space.

Please note, that the root disk can be the volume disk if specified.
Images can require the flavor they are running on to have a certain amount of RAM and disk space to work. These can be set when uploading or creating an image.

The current list of de.NBI flavors is described [here.](./flavors.md)

## Available Images

Most common operating systems are available on all cloud-locations (Ubuntu, CentOS...).
These images are configured, tested and ready for use.
If you find an image missing, feel free to upload your own image or contact de.NBI-Support.

## Snapshots

It is possible to create Snapshots from running instances.
Snapshots save the current status of a VM and can be used as a backup mechanism. 
These snapshot images are displayed as regular images in the image overview and can be used like regular images.

