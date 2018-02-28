# Using and managing images

## Introduction
To start a virtual machine in Openstack a virtual machine image (brief: image) is required. Images are files that contain a bootable operating system. Cloud images are available for various operating systems like Ubuntu or CentOS. They are usually separated from the normal installation images. For Ubuntu and CentOS7 the cloud images can be found here: [Ubuntu](https://cloud-images.ubuntu.com/) [CentOS7](https://cloud.centos.org/centos/7/images/?C=M;O=D). Please mind that our Openstack installation provides default images that can be used.

## Adding images to Openstack

To add an image to Openstack open the Openstack dashboard, go to Compute and then Images. In the upper right corner click "Create Image".
![Glance image overview](/img/User/images_overview.png)

 Fill in the fields in the opened form. For informations to single fields please refer to the following list. All fields not mentioned here are neither required by Openstack nor suggested to be used by normal users by us .

*  Image Name: Name of the image that is displayed in the image list. Please use a self describing name (e.g. Ubuntu_17.04)

*  Image Description: [optional] Description of the image. Could contain for example use cases.

*  File: Image file of the image, will be uploaded from the local file system.

*  Format: Format of the uploaded image file. For details on file formats please refer to the Image file format section.

*  Minimum Disk: Minimal amount of disk space required for the image to run. Will restrict the flavors the image can be run on.

*  Minimum RAM: Same as Minimum Disk, bur for RAM. Also restricts the applicable flavors.

*  Visibility: Whether the image is publicly available or not. Please only use private images, although the default might be different.

*  Protected: Protects the image from unintended deletion.

![Create Image](/img/User/create_image.png)

The metadata can be left empty. For a more detailed documentation please refer to the official documentation: [Openstack image documentation](https://docs.openstack.org/image-guide/introduction.html).
To finish image creation please click Create Image.
The image should no be visible in the Images list.

## Image file format

Image files come in different formats. Openstack supports a wide variety of image file formats.
The most common formats for images are qcow2 and raw. Please mind that files in iso format usually do not work as they are often used for regular OS installation and not prepared for cloud environments. For further informations please refer to the [Openstack image documentation](https://docs.openstack.org/image-guide/introduction.html).


## Image Management

All uploaded Images can be seen under Project -> Compute -> Images. Images can be created and deleted here. In addition it is possible to launch instances with a specific image. It is also to create a volume based on an image.

## Images on volumes and ephemeral disks

When creating a virtual machine it can either be created on an ephemeral disk using local storage or on a volume. The size of the ephemeral disk is determined by the used flavor, the size of the volume can be chosen by the user. The decision of whether to use ephemeral storage or a volume for the vm can be made in the Launch Instance dialog in the Source section. If no new volume is created on startup the ephemeral disk is used, otherwise the only the volume is used and there will be no ephemeral disk for this instance. When using a volume disk Openstack currently does not check if the volume has sufficient space for the image but it still checks if the selected flavor has a sufficient amount of ephemeral disk space although the ephemeral disk is not used.

## Images and Flavors

When creating a VM the user has to select a flavor. This flavor defines the resources a virtual machines has. There are various flavors predefined in Openstack. They vary in the number of available vCPUs, RAM and their disk setup.


*  vCPU: Number of CPUs available in the VM

*  RAM: Amount of RAM available in the VM

*  Total Disk: Amount of disk space available on root disk and ephemeral disk

*  Root Disk: Root disk space

*  Ephemeral Disk: Ephemeral disk space

Please note that the root disk can be the volume disk if specified.
Image can require the flavor they are running on to have a certain amount of RAM and disk space to work. These can be set when uploading or creating an image.

## Available Images

There are currently various images publicly available. Most of them are either for testing or serve special purposes. Public images for common uses are the following:

*  Ubuntu 16.04 Xenial 2017/04/19: Generic Ubuntu cloud image

## Snapshots

It is possible to create Snapshots from running instances. These snapshot images are displayed as regular images in the image overview and can be used like regular images.
