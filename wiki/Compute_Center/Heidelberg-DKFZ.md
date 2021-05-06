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
To access your project, use Elixir as authentication provider. After
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
None of your VMs will be directly visible and accessible from the internet. Therefore, please make sure that you add your public ssh key to the [central portal](https://cloud.denbi.de/). This is important as you will login to our jumphost first before connecting to your VMs. The jumphost account will only be created after adding a public ssh key to the central portal.

#### Linux-based host
To connect to one of your VMs, you have to use our jumphost denbi-jumphost-01.denbi.dkfz-heidelberg.de with your elixir login name (not your elixir id!):

    ssh -A -i YOUR-SSH-KEY USERNAME@denbi-jumphost-01.denbi.dkfz-heidelberg.de

**Example:** ssh -A -i ~/.ssh/denbi-cloud.key elixir1234@denbi-jumphost-01.denbi.dkfz-heidelberg.de

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
Please use your elixir username here.

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
      # Use your Elixir login name
      User ELIXIR_USERNAME
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
      # Use your Elixir login name
      User ELIXIR_USERNAME
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
