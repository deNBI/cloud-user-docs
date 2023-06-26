# de.NBI Cloud DKFZ Heidelberg
Welcome to the de.NBI Cloud site DKFZ Heidelberg. In the following guide we want
to give you a quick introduction how to use our cloud site.

Please note, you are responsible for everything that happens with the virtual
machines (VMs) you deploy! We as resource provider are not liable for
anything and do not give any guarantees.

## How to get in contact with us
In case you have questions or want to give us any kind of feedback, please
contact us via denbi-cloud(at)dkfz-heidelberg.de.

## Access to the de.NBI Cloud DKFZ Heidelberg
### OpenStack Dashboard
The OpenStack dashboard gives you all information about your
project, e.g. your available resources, your virtual machines etc. The
dashboard is available [here](https://cloud.denbi.dkfz-heidelberg.de).
To access your project, use LifeScience as authentication provider. After
authentication you will be redirected to the OpenStack dashboard.

### SSH-Keys
As a first step make sure that you import a public ssh-key into your
OpenStack project (**Project - Compute - Key Pairs - Import
Key Pair**) so that you can access your VMs later on.

### Deploy your VMs
The networks are already pre-configured, so you can directly start and deploy
your VMs. Therefore go to **Project - Compute - Instances** and choose the
button **"Launch Instance"** on the right side. Now you have to provide
information at least in the categories **Details, Source and Flavor**.

  **Details:**

  - In the field "Instance Name", assign a name to your VM

  **Source:**

  - Choose "Image" as "Boot Source"
  - Set "Create New Volume" to No
  - Choose an appropriate image from the list (e.g. CentOS)

  **Flavor:**

  - Choose a Flavor from the list that fits your resource requests (e.g de.NBI
  default provides 2 cores with 4GB of RAM)

Now hit the button "Launch Instance". The VM will be deployed and accessible
in a few seconds. To connect to your VM you need to assign a floating ip
address to the machine. Therefore click on the arrow on the right side of the
spawning VM, choose "**Associate Floating IP**" and use one available
floating ip addresses from the drop-down menu.

**Hint:** To connect to one of your VMs without a floating ip address you have to
assign at least one floating ip address to another of your machines. As soon
as you are connected to this machine you are inside of your project network
and can connect to VMs without any floating ip address.

### Connect to your VMs
#### Prerequisites
None of your VMs will be directly visible and accessible from the internet. Therefore, please make sure that you add your public ssh key to the [central portal](https://cloud.denbi.de/). This is important as you will login to our jumphost first before connecting to your VMs. The jumphost account will only be created after adding a public ssh key to the central portal and you must be a member of a project that is located at the Heidelberg DKFZ.

#### Linux-based host
To connect to one of your VMs, you have to use our jumphost denbi-jumphost-01.denbi.dkfz-heidelberg.de with your LifeScience login name (not your Elixir ID!):

    ssh -A -i YOUR-SSH-KEY USERNAME@denbi-jumphost-01.denbi.dkfz-heidelberg.de

**Example:** ssh -A -i ~/.ssh/denbi-cloud.key lifescience1234@denbi-jumphost-01.denbi.dkfz-heidelberg.de

From the jumphost you can connect to each of your VMs which has an attached
floating ip address.

On some OS the ssh-agent is not running by default (like on MacOS), so you have to start the agent
before. You then can use the ssh-agent to forward the ssh key to the target host. First, check that
the ssh-agent is running:

    eval `ssh-agent -s`
    Agent pid 14655

Then, check that your key is known by the agent (in this case, it has none):

    ssh-add -l
    The agent has no identities.

Add your ssh key to the ssh-agent:

    ssh-add YOUR-SSH-KEY-FILE

If your key is protected by a passphrase, you will have to enter it now:

    Enter passphrase for YOUR-SSH-KEY-FILE:
    Identity added: YOUR-SSH-KEY-FILE (YOUR-SSH-KEY-FILE)

#### Windows-based host
If you want to connect from a Windows-based system you can use Putty
(https://www.putty.org/) to connect to the jumphost and your virtual machines.

In the field **Host Name** you have to enter the name of our jumphost:

    denbi-jumphost-01.denbi.dkfz-heidelberg.de

Under **Connection - Data** you can choose the username for the auto-login.
Please use your LifeScience username here.

In the section **Connection - SSH - Auth** you can provide your SSH-key.
Please make sure that you also check the option **Allow agent forwarding** so
that you can connect to your VM.

When you connect to our jumphost for the first time you may get a warning about
accepting the servers host key. Please confirm with yes.

### Create Volumes
If you need more disk space than the initial image provides (20GB), one
way is to create a volume and attach it to your VM. Please keep in mind that
a volume can only be attached to one VM at the same time. The advantage of a
volume is that it will be available also after you deleted your VM. So you can
use it to store data temporally.

To create a volume choose **Project - Compute - Volumes** followed by **Create
Volume** on the right side. Now assign a name to your volume and set the size
according to your needs. After the successful creation of the  volume you have
to attach it to your VM. Choose the arrow on the right side of the created
volume and select **Attach Volume**. In the new window you have to choose your
VM from the drop-down menu under **Attach to Instance**.

On your VM you now have to make a filesystem on the device so that you can
mount it to your machine. Use e.g. mkfs to make an ext4 filesystem:

    sudo mkfs.ext4 /dev/vdb

After creating the filesystem you can mount the filesystem to your VM and start
using it:

    sudo mount /dev/vdb /mnt

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
  - Please select "isilon-denbi".

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
  - Please fill in the floating ip address of your VM you want to grant access to the NFS share.

#### Access your NFS share
In order to use your created NFS share you have to mount it to your VMs.
Click on the created share in the **Shares** section of the OpenStack
dashboard to get information about the complete mount path. Under the
**Export locations** section you will find the complete path to your NFS share.

You can mount the share with the following command:

    sudo mount -o vers=4.0 manila-prod.isi2.denbi.dkfz.de:/ifs/denbi/prod/YOUR-SHARE /mnt/

Alternatively you can add the mount path to the "/etc/fstab". Make sure that
you use NFS version 4.0.

Please make sure that your user (depending on the used distribution: centos,
debian, ubuntu) is the owner of the NFS share. Therefore run the following
command to set the user as owner of the NFS share:

    sudo chown centos:centos /mnt/

**Hint** This example is for a Centos based image.

### Distribution logins
Please be aware that our images are shipped with the standard users for the
respective Linux distribution. Here you  can see a list of standard users for
some common distributions:

  - **CentOS**: centos
  - **Ubuntu**: ubuntu
  - **Debian**: debian

### Connecting to your VMs directly
To easily connect directly to your VMs via our jumphost you can configure a
ProxyJump inside of your **local ~/.ssh/config**:

    # Access to the de.NBI jumphost
    Host denbi-jumphost-01.denbi.dkfz-heidelberg.de
      # Use your LifeScience login name
      User LIFESCIENCE_USERNAME
      # Use your ssh-key file
      IdentityFile YOUR-SSH-KEY-FILE
      # Send a keep-alive packet to prevent the connection from being terminated
      ServerAliveInterval 120

    Host 10.133.24* 10.133.25*
      # Use jumphost as proxy
      ProxyJump denbi-jumphost-01.denbi.dkfz-heidelberg.de
      # Use your ssh-key file
      IdentityFile YOUR-SSH-KEY-FILE
      # Send a keep-alive packet to prevent the connection from being terminated
      ServerAliveInterval 120

Please make sure that your local ssh-client is up to date, ProxyJump was
introduced in OpenSSH version 7.3.

You now should be able to connect to your VM directly using the floating ip
address:

    ssh centos@10.133.2xx.xxx

## File transfer into the de.NBI cloud
In case you want to transfer local data into the cloud you can use rsync, scp,
etc. combined with a SOCKS proxy with one of your VMs as the target host. The
jumphost itself is not meant to store data. In case you have large amounts of
data please contact us.

## Advanced Section
This section includes some more advanced topics and configurations.

### Setting up a SOCKS proxy
In some cases it would also make sense to configure a permanent SOCKS proxy to
communicate with your VMs behind the jumphost, e.g. when using web
applications etc. As long as you have an open SOCKS connection to the
jumphost you can directly connect to your VMs from a different console. In the
following example socat is used but also netcat (nc) works in a similar way.
Add the following lines to your **local ~/.ssh/config**:

    # Access to the de.NBI jumphost
    Host denbi-jumphost-01.denbi.dkfz-heidelberg.de
      # Use your LifeScience login name
      User LifeScience_USERNAME
      # Use your ssh-key file
      IdentityFile YOUR-SSH-KEY-FILE
      # Open a SOCKS proxy locally to tunnel traffic into the cloud environment
      DynamicForward localhost:7777
      # Forward locally managed keys to the VMs which are behind the jumphosts
      ForwardAgent yes
      # Send a keep-alive packet to prevent the connection from being terminated
      ServerAliveInterval 120

    # Access to de.NBI cloud floating IP networks via SOCKS Proxy
    Host 10.133.24* 10.133.25*
      # Tunnel all requests through dynamic SOCKS proxy
      ProxyCommand /usr/bin/socat - socks4a:localhost:%h:%p,socksport=7777
      # Use your ssh-key file
      IdentityFile YOUR-SSH-KEY-FILE
      # Forward locally managed keys
      ForwardAgent yes
      # Send a keep-alive packet to prevent the connection from being terminated
      ServerAliveInterval 120

Now you can connect to the jumphost the same way you usually do. As
long as you have this connection open you can directly connect to one of your
VMs from another terminal by specifying the username and ip address without
the need to first connect to the jumphost:

    ssh centos@10.133.2xx.xxx

### Using the OpenStack API
First, you will need to request a password to use the OpenStack API,
therefore write a mail to the support team at <denbi-cloud@dkfz-heidelberg.de>.
Second, the API is not directly accessible from the outside, so the only way to
access the API from a local machine is through the jumphost. So make sure you've
configured your SOCKS proxy as described before. In addition you will need to
configure your environment to use the SOCKS proxy for the API requests.
Therefore set your environment variables for the http/https proxy:

    export http_proxy=socks5h://localhost:7777
    export https_proxy=socks5h://localhost:7777
    export no_proxy=localhost,127.0.0.1,::1

Now, if you have an active SOCKS connection to the jumphost, you should be
able to use the OpenStack API from your local machine.

### Terraform

#### Prerequisites
Install Terraform either via your distribution or by downloading it from the [website](https://www.terraform.io/downloads.html).


Similar to using the OpenStack CLI you will need a proper ssh config to use a SOCKS proxy as described above. To be able to use Terraform please download the openstack.rc file (v3) for your OpenStack project, source it and export the SOCKS proxy in your shell environment:
```bash
source openrc.sh
export https_proxy=socks5://localhost:7777
export http_proxy=socks5://localhost:7777
```

Please make sure to **use socks5** instead of socks5h as you might would use with the OpenStack CLI.


Furthermore we have to tell Terrafrom which providers we want to use. Therefor create a `versions.tf` file in your working directory with the following content if you use Terraform >= 0.13:
```
terraform {
  required_providers {
    openstack = {
      source = "terraform-provider-openstack/openstack"
    }
  }
  required_version = ">= 0.13"
}
```


#### Basic Terraform example
We will create a `main.tf` file containing some basic tasks like uploading our public ssh key, creating a new sandbox VM and also attaching a floating ip address to the newly created VM.
```
# Deploy public ssh key
resource "openstack_compute_keypair_v2" "ssh-key" {
  name       = "ssh-key"
  public_key = "PUT_YOUR_PUBLIC_KEY_HERE"
}


# Deploy sandbox VM
resource "openstack_compute_instance_v2" "sandbox-vm" {
  name            = "sandbox"
  image_name      = "IMAGE_NAME"
  flavor_name     = "FLAVOR_NAME"
  key_pair        = "ssh-key"
  security_groups = ["default"]

  network {
    name = "NETWORK_NAME"
  }
}


resource "openstack_networking_floatingip_v2" "fip" {
  pool = "public"
}


# Associate floating ip
resource "openstack_compute_floatingip_associate_v2" "fip" {
  floating_ip = "${openstack_networking_floatingip_v2.fip.address}"
  instance_id = "${openstack_compute_instance_v2.sandbox-vm.id}"
}
```

The configuration can be verified with `terraform validate`. Please also make sure to run `terraform init` if you are starting in a fresh directory so that the latest OpenStack plugins will be available.

#### Working with Terraform
To apply a Terraform configuration simply run `terraform apply`. You will see an overview of the tasks to do. You have to confirm the listed actions by typing `yes`.

Each time you change the `main.tf` configuration file and run `terraform apply` you will see which changes to the current state of your infrastructure will be applied.

To get a complete overview of the current state you can run `terraform show`.

You can destroy all resources defined in your configuration file with the `terraform destroy`. Terraform will list all resources which will be deleted. You have to confirm the listed actions by typing `yes`. Terraform will not touch any OpenStack resources that were defined outside of your Terraform configurations.

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

### Upload your own Linux images
If you need an extra Linux image we do not provide, you also can upload your
own images via **Project - Compute - Images**. Select **Create Image** and
choose a name and the path for the image and also make sure that you choose
the correct format (typically qcow2). If there are special requirements for
your image, you can specify the minimum disk size and also the minimum
amount of RAM. After the successful upload only the members of your project
can use the image.
