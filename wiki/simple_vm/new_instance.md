# Starting a virtual machine

On this page we guide you through the options you have when starting a virtual machine.  
If you are a member of a simple vm project you can start a virtual machine at the "New Instance" tab.  
You may need to reload the website if you can not see the tab.

## Mandatory configuration
![overview_one](./img/new_instance/new_instance_overview_one.png)

### 1. Overview
Here you get an overview of your allocated ressources and how much of it is currently in use. If your allocated ressources do not allow to start a virtual machine, your PI may request more ressources.

### 2. Name
Here you may name your virtual machine or use a randomly generated name. An unique id will be appended after starting your virtual machine.

### 3. Flavor
Here you may choose the flavor for you virtual machine. Flavors dictate the ressources your virtual machine will be started with. For more information about flavors please visit the [flavor wiki page](../Concept/flavors.md).

### 4. Image
Here you may choose the image your virtual machine will be started with. Images are basically the operating system and tool packages which will be installed on your virtual machine. The images listed here are the ones provided by de.NBI and your created snapshots. For more information about images and snapshots, please visit the [wiki page](./snapshots.md).

## Optional configuration
![overview_two](./img/new_instance/new_instance_overview_two.png)

### 1. Volumes
Here you may create, attach and mount a new volume or attach and mount an already existing volume.  
For more information about volumes, please visit the [volume wiki](./volumes.md) page.

Click on `New Volume` and you will see:
![vol_new](./img/new_instance/new_instance_vol_new.png)
 You may name your volume, choose its mountpath, which is the path to the data saved on the volume and choose the amount of storage.  

Click on `Attach existing Volume` and you will see:
![vol_ex](./img/new_instance/new_instance_vol_ex.png)
You may choose its mountpath, which is the path to the data saved on the volume.  

After adding a volume you will see an overview of your chosen volumes:
![vol_done](./img/new_instance/new_instance_vol_done.png)

### 2. Conda tools
![conda](./img/new_instance/new_instance_conda.png)
Here you may choose multiple conda, bioconda and anaconda tools which will be installed on your machine at startup. For more information, please visist the [customization wiki page](./customization.md#conda).

### 3. Research environments
![resenv](./img/new_instance/new_instance_resenv_name.png)
Here you may choose from different browser based research environments respectively web IDEs, which will be installed on your machine at startup. For more information, please visist the [customization wiki page](./customization.md#research-environments).

### 4. Optional parameters
![optionals](./img/new_instance/new_instance_optional.png)
Here may find some additional options for your virtual machine.
#### MOSH / UDP ports
Here you are able to open UDP ports and have MOSH installed on your virtual machine. Open UDP ports allow for better mobile usage and MOSH is used/needed to connect to your virtual machine via UDP. For more information on using UDP ports and MOSH, please visist the [respective wiki page](../Tutorials/Mosh/index.md).

## Start VM
Here you finally may start your virtual machine. After a short time, you will be redirected to the [Instance Overview](./instance_overview.md) page.
