# de.NBI Cloud Heidelberg
Welcome to the de.NBI Cloud site Heidelberg. In the following guide we want 
to give you a quick introduction how to use our cloud site.

Please note, you are responsible for everything that happens with the virtual
machines (VMs) you deploy! We as resource provider are not liable for 
anything and do not give any guarantees. It is anticipated to have a more 
sophisticated user agreement in 2018.

## How to get in contact with us
In case you have questions or want to give us any kind of feedback, please 
contact us via <denbi-cloud@bioquant.uni-heidelberg.de>.

## Access to the de.NBI Cloud Heidelberg
### OpenStack Dashboard
The OpenStack dashboard gives you all information about your 
project, e.g. your available resources, your virtual machines etc. The 
dashboard is available [here](https://denbi-cloud.bioquant.uni-heidelberg.de).
To access your project, use Elixir as authentication provider. After 
authentication you will be redirected to the OpenStack dashboard.

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
#### Linux-based host
None of your VMs is directly visible and accessible from the internet. To 
connect to one of your VMs, you have to use our jump-host
denbi-jumphost-01.bioquant.uni-heidelberg.de with your elixir login name (not
your elixir id!):

    ssh -A -i YOUR-SSH-KEY USERNAME@denbi-jumphost-01.bioquant.uni-heidelberg.de
    
**Example:** ssh -A -i ~/.ssh/denbi-cloud.key elixir1234@denbi-jumphost-01.bioquant.uni-heidelberg.de

From the jump-host you can connect to every of your VMs which has an 
associated floating ip address.

#### Windows-based host
If you want to connect from a Windows-based system you can use Putty 
(http://www.putty.org/) to connect to the jump-host and your virtual machines.

In the field **Host Name** you have to enter the name of our jump-host:

    denbi-jumphost-01.bioquant.uni-heidelberg.de
    
Under **Connection - Data** you can choose the username for the auto-login. 
Please use your elixir username here.

In the section **Connection - SSH - Auth** you can provide your SSH-key. 
Please make sure that you also check the option **Allow agent forwarding** so
that you can connect to your VM.

When you connect the first time to our jump-host you may get a warning 
related server host keys. Please confirm with yes.

### Create and configure a NFS share for your project
In case you need a NFS share to store big amounts of data and share it within
your project, you can use OpenStack to create and manage the share.

#### Create a NFS share
To create a NFS share choose the section **Shares** and click on **Create 
Share**. In the popup you have to provide the following information:

  **Share Name:**
  - Provide a share name.
  
  **Share Protocol:**
  - Please use the preselected "NFS" as protocol.
  
  **Size (GiB):**
  - Provide the size of the share. Info: You have an overall quota for NFS 
  shares on your project. Please make sure that you set the size below the 
  project quota.

  **Share Type:**
  - Please select "default".
  
  **Availability Zone:**
  - Please select "nova".

#### Manage access rules for your NFS share
After the creation of a NFS share, the share will not be accessible by anyone
. To grant your VMs access to the share you have to configure the access rules.

**Important: Please make sure to keep the access rule list of your NFS share up
 to date**, so that only your VMs can access the share.

To manage the access rules click on the **arrow** on the right side of your 
newly created NFS share and choose **Manage rules**. Now you have to choose 
**Add rule**. In the popup you have to provide the following information:

  **Access Type:**
  - Select ip to allow a certain VM access to the share.
  
  **Access Level:**
  - Choose **read-write** or **read-only** appropriate to your needs. In some
   cases it may make sense that specific VMs just get read-only permissions.
  
  **Access to**
  - Please fill in the ip address of your VM you want to grant access to the 
  NFS share.
  
#### Access your NFS share
In order to use your created NFS share you have to mount it to your VMs. 
Click on the created share in the **Shares** section of the OpenStack 
dashboard to get information about the complete mount path. Under the 
**Export locations** section, please choose the first **Path**. It usually has
a format like:
     
     isiloncl1-487.denbi.bioquant.uni-heidelberg.de:/ifs/denbi/manila-prod/share-123456789

You can mount the share with the following command:

    sudo mount -o vers=4.0 isiloncl1-487.denbi.bioquant.uni-heidelberg.de:/ifs/denbi/manila-prod/YOUR-SHARE /mnt/
    
Alternatively you can add the mount path to the "/etc/fstab". Make sure that 
you use NFS version 4.0.

Please make sure that your user (depending on the used distribution: centos, 
debian, ubuntu) is the owner of the NFS share. Therefore run the following 
command to set the user as owner of the NFS share:

    sudo chown centos:centos /mnt/
    
**Hint** This example is for a Centos based image.

### Distribution logins
Please take care, as for now, that our images are shipped with the standard 
users for the respective Linux distribution. Here you can see a list of 
standard users for some common distributions:
 
  - **CentOS**: centos
  - **Ubuntu**: ubuntu
  - **Debian**: debian

## File transfer into the de.NBI cloud
In case you need to transfer data into the cloud we use a transfer host which
is connected to your NFS share. Please contact us if you want to transfer big
amounts of data.

## Advanced Section
This section includes some more advanced topics and configurations.

### Setting up a SOCKS proxy
To make it easier to connect to your VMs you can set up an SOCKS proxy with 
AgentForwarding. As long as you have an open SOCKS connection to the 
jumphost you can directly connect to your VMs without the need to login to 
the jumphost each time. In the following example socat is used. Add the 
following lines to your **local ~/.ssh/config**:

    # Access to the de.NBI jumphost
    Host denbi-jumphost-01.bioquant.uni-heidelberg.de
      # Use your Elixir login name
      User ELIXIR_USERNAME
      # Use your ssh key for agent forwarding
      IdentityFile YOUR-KEY-FILE
      # Open a SOCKS proxy locally to tunnel traffic into the cloud environment
      DynamicForward localhost:7777
      # Forward locally managed keys to the VMs which are behind the jumphosts
      ForwardAgent yes
      # Send a keep-alive packet to prevent the connection from terminating
      ServerAliveInterval 120
      
    # Access to de.NBI cloud floating IP networks via SOCKS Proxy
    Host 172.16.6* 172.16.7*
      # Tunnel all requests through dynamic SOCKS proxy
      ProxyCommand /usr/bin/socat - socks4a:localhost:%h:%p,socksport=7777
      # Use your ssh key for agent forwarding
      IdentityFile YOUR-KEY-FILE
      # Forward locally managed keys
      ForwardAgent yes
      # Send a keep-alive packet to prevent the connection from terminating
      ServerAliveInterval 120

Now you can connect to the jumphost the same way you usually do. As 
long as you have this connection open you can directly connect to one of your 
VMs from another terminal by specifying the username and ip address without 
the need to first connect to the jumphost:

    ssh centos@172.16.7x.xxx 

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

On your VM you now have to setup a filesystem on the device so that you can 
mount it to your machine. Use mkfs to make an ext4 filesystem:

    mkfs.ext4 /dev/vdb
    
After this step you can mount the filesystem to your VM and start using it:

    sudo mount /dev/vdb /mnt

### Upload your own Linux images
If you need an extra Linux image we do not provide, you also can upload your 
own images via **Project - Compute - Images**. Select **Create Image** and 
choose a name and the path for the image and also make sure that you choose 
the correct format (typically qcow2). If there are special requirements to 
your image, you can specific the minimum Disk size and also the minimum 
amount of RAM. After the successful upload only the members of your project 
can use the image.
