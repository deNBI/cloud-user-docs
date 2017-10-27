# de.NBI Cloud Heidelberg
Welcome to the de.NBI Cloud site Heidelberg. In the following guide we want 
to give you a quick introduction how to use our cloud site.

Please note, you are responsible for everything that happens with the virtual
machines (VMs) you deploy! We as resource provider are not liable for 
anything and do not give any guarantees. It is anticipated to have a more 
sophisticated user agreement available till the end of 2017.

## How to get in contact with us
In case you have questions or want to give us any kind of feedback, please 
contact us via <denbi-cloud@bioquant.uni-heidelberg.de>.

## Access to the de.NBI Cloud Heidelberg
### OpenStack Dashboard
The OpenStack dashboard gives you all information about your 
project, e.g. your available resources, your virtual machines etc. The 
dashboard is available [here](https://denbi-cloud.bioquant.uni-heidelberg.de/).
To log in to your project, use the domain “bioquant” and your credentials.

### SSH-Keys
As a first step make sure that you import a public ssh-key into your 
OpenStack project (**Project - Compute - Access & Security - Key Pairs - Import 
Key Pair**) so that you can access your VMs later on.

### Deploy your VMs
The networks are already preconfigured, so you can directly start and deploy 
your VMs. Therefore go to **Project - Compute - Instances** and choose the 
button **"Launch Instance"** on the right side. Now you have to provide 
information at least in the categories **Details, Source and Flavor**.

  **Details:**
  
  - In the field "Instance Name", assign a name to your VM
  
  **Source:**
  
  - Choose "Image" as "Boot Source"
  - Set "Create New Volume" to No
  - Choose an appropriate image from the list (e.g. CentOS 7.4)
  
  **Flavor:**
  
  - Choose a Flavor from the list that fits your resource requests (e.g de.NBI 
  default - that would be 2 cores with 4GB of RAM)
  
Now hit the button "Launch Instance". The VM will be deployed and accessible
in a few moments. To connect to your VM you need to assign a floating ip 
address to the machine. Therefore click on the arrow on the right side of the
spawning VM, choose "**Associate Floating IP**" and use one available
floating ip addresses from the drop-down menu.

**Hint:** To connect to one of your VMs without a floating ip address you have to 
assign at least one floating ip address to another of your machines. As soon 
as you are connected to this machine you are inside of your project network 
and can connect to VMs without any floating ip address.

### Connect to your VMs
None of your VMs is directly visible and accessible from the internet. To 
connect to one of your VMs, you have to use our jump-host
denbi-jumphost-01.bioquant.uni-heidelberg.de (129.206.69.162) with the same 
credentials you used for the OpenStack dashboard:

    ssh -A -i YOUR-SSH-KEY USERNAME@denbi-jumphost-01.bioquant.uni-heidelberg.de
    
**Example:** ssh -A -i ~/.ssh/denbi-cloud.key bq_00denbi@denbi-jumphost-01.bioquant
.uni-heidelberg.de

From the jump-host you can connect to every of your VMs which has an 
associated floating ip address.

### How to change your password
If you want to change the password of your "denbi" account we assigned to 
you, please connect to appl2:

    ssh USERNAME@appl2.bioquant.uni-heidelberg.de
    
On appl2 you can change the password using "passwd".

### Access your NFS-Share
In case you have requested a NFS-Share for your project you have to mount it 
to your VMs:

    sudo mount -o vers=4.0 isiloncl1-487.denbi.bioquant.uni-heidelberg.de:/ifs/denbi/YOUR-SHARE /mnt/
    
Or add the mount-point to the "/etc/fstab". Make sure that you use NFS 
version 4. This share is accessible for all members of your project and 
should be used for project data and for sharing big data sets between your VMs.

### Distribution logins
Please take care, as for now, that our images are shipped with the standard 
users for the respective Linux distribution. Here you can see a list of 
standard users for some common distributions:
 
  - **CentOS**: centos
  - **Ubuntu**: ubuntu
  - **Debian**: debian

## File transfer into the de.NBI cloud
In case you need to transfer data into the cloud we use a transfer host which
is connected to your NFS-Share. Please contact us if you want to transfer big
amounts of data.

## Advanced Section
This section includes some more advanced topics and configurations.

### Adding multiple SSH-Keys
To access your VM you have to provide a public ssh-key. In the deployment 
step of your VM you can choose which public ssh-key you want to use for your 
VM in the section **Key Pair**.

In case you want to directly deploy a VM and give access to more than one 
user you can use the section **Configuration - Customization Script** in the 
deployment part. Here you have to list the full **public keys** in the 
following format:

    #cloud-config
    ssh_authorized_keys:
        - Full public ssh-key of User-1
        - Full public ssh-key of User-2

After the successful deployment of the VM, user 1 and user 2 will have access 
to the VM.

### Create Volumes
If you do need more disk space than the initial image provides (20GB), one 
way is to create a Volume and attach it to your VM. Please keep in mind that 
a volume can only be attached to one VM at the same time. Furthermore the 
maximal size of a volume is 50GB. The advantage of a volume is that it will 
be available also after you deleted your VM. So you can use it to store data 
temporally.

To create a Volume go to **Project - Compute - Volumes** and choose **Create 
Volume** on the right side. Now assign a name to your volume and set the size
according to your needs (max 50GB). After the successful creation of the 
volume you have to attach it to your VM. Choose the arrow on the right side 
of the created volume and select **Attach Volume**. In the new window you 
have to choose your VM from the drop-down menu under **Attach to Instance**.

### Upload your own Linux images
If you need an extra Linux image we do not provide, you also can upload your 
own images via **Project - Compute - Images**. Select **Create Image** and 
choose a name and the path for the image and also make sure that you choose 
the correct format (typically qcow2). If there are special requirements to 
your image, you can specific the minimum Disk size and also the minimum 
amount of RAM. After the successful upload only the members of your project 
cane use the image.