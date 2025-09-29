# de.NBI Cloud Berlin
Welcome to the de.NBI Cloud site in Berlin. This guide provides a quick introduction to using our cloud platform.

### Disclaimer

You are solely responsible for all activities related to the virtual machines (VMs) you deploy. As the resource provider, we are not liable for any issues and offer no guarantees. We strongly recommend making your setup as reproducible as possible from the start.

### How to Contact Us
For questions or feedback, please email us at <denbi-cloud@bih-charite.de>.

## Access to the de.NBI Cloud Berlin
### OpenStack Dashboard
The OpenStack dashboard gives you all information about your 
project, e.g. your available resources, your virtual machines etc. The 
dashboard is available [here](https://denbi-cloud.bihealth.org).
To access your project, use LifeScience AAI as authentication provider. After 
authentication you will be redirected to the OpenStack dashboard.

**Important Note** We block incoming connections from several countries. If you cannot access the dashboard or the jumphost from outside Germany, please contact us for assistance.

## Deploying Your First VM
The networks are pre-configured, so you can immediately begin deploying VMs.

1. Navigate to Project -> Compute -> Instances.

2. Click the "Launch Instance" button on the right.

3. You must fill in the information in the Details, Source, and Flavor tabs.

### 1. Details Tab

- Instance Name: Assign a descriptive name to your VM.
  
### 2. Source Tab
  
- Boot Source: Select "Image".
- Create New Volume: This choice determines where your VM's disk is stored.

  - No (Recommended for temporary VMs): Your VM's disk will be created on the local storage of the host machine (hypervisor). It is limited to 20 GB.

**Warning:** With this option, your VM cannot be recovered in the event of a hardware failure on that specific host.

  - Yes (Recommended for persistent VMs): Your VM's disk will be created as a persistent volume on our separate, storage system. It can be larger than 20 GB.

**Warning:** Please do not create initial volumes larger than 50 GB. You can always attach additional data volumes later.

- Image Name: Choose an operating system image from the list (e.g., Ubuntu-24).  
  
### 3. Flavor Tab
  
- Choose a "Flavor" that matches your required CPU and RAM resources (e.g., de.NBI default provides 2 CPU cores and 4 GB of RAM).

### 4. Networks Tab
  
- It is recommended to select your project's internal network (e.g., yourProject-network).

Click "Launch Instance". Your VM will be deployed and ready in a few moments.
### 5. Key Pair

- Please add your key pair to the instance
  
  
## Assigning a Floating IP
  
To connect to your VM from our jumphost, you must assign it a "Floating IP" address.

1. In the Instances list, find your newly created VM.

2. Click the dropdown arrow on the right and select "Associate Floating IP".

3. Choose an available IP from our "public" floating ip pool `10.57.200.0 /21` click "Associate".

**Hint:** To connect to a VM that does not have a Floating IP, you must first SSH into another VM within the same project that does have a Floating IP. Once connected, you are inside your private project network and can access all other internal VMs.

## Connect to your VMs with ssh

Your VMs are not directly accessible from the public internet. You must first connect to our jumphost server and then connect to your VM from there.
- Jumphost Address: denbi-jumphost-01.bihealth.org
- Jumphost Username: Your LifeScience AAI login name (If you are unsure, check your  [profile page](../portal/user_information.md).

### Prerequisites: SSH Keys

You must configure your SSH keys in two places:

1. de.NBI Portal (for Jumphost Access): Add your public SSH key at https://cloud.denbi.de/portal/.
2. OpenStack Project (for VM Access): Import the same public SSH key into your OpenStack project by navigating to Project -> Compute -> Key Pairs -> Import Key Pair.

1. de.NBI Portal (for Jumphost Access): Add your public SSH key at https://cloud.denbi.de/portal/.
2. OpenStack Project (for VM Access): Import the same public SSH key into your OpenStack project by navigating to Project -> Compute -> Key Pairs -> Import Key Pair.

### Default Usernames for Common Images
Our standard images use default usernames. Use the correct one when connecting to your VM:

- **Rocky**: rocky
- **Ubuntu**: ubuntu

### SSH Configuration for Windows 10/11

Windows includes OpenSSH by default, which can be used in PowerShell. Create a configuration file at ```$HOME\.ssh\config``` 

=======

You can create it with a text editor like Notepad or by using this PowerShell command (be sure to replace the placeholder content): 

```Set-Content -Path $HOME\.ssh\config -Value '<add file content here>'```

Add the following to your config file, replacing the bracketed values:

```bash
# ----- Connection to the de.NBI Jumphost -----
Host denbi-jumphost-01.bihealth.org
    HostName denbi-jumphost-01.bihealth.org
    User {Your_LifeScience_Login}
    IdentityFile {C:\path\to\your\private_key} # e.g., C:\Users\YourUser\.ssh\id_rsa

# ----- Connection to your VM via the Jumphost -----
Host {A_Friendly_Name_For_Your_VM}
    HostName {10.57.XXX.XXX} # The Floating IP of your VM
    User {ubuntu} # or rocky, etc.
    IdentityFile {C:\path\to\your\private_key}
    ProxyJump denbi-jumphost-01.bihealth.org
```

Save the file. You can now connect directly to your VM from PowerShell with:

```console
ssh {A_Friendly_Name_For_Your_VM}
```

### SSH Configuration for Linux / macOS

```bash
# ----- Connection to the de.NBI Jumphost -----
Host denbi-jumphost-01.bihealth.org
    HostName denbi-jumphost-01.bihealth.org
    User {Your_LifeScience_Login}
    IdentityFile {/path/to/your/private_key} # e.g., ~/.ssh/id_rsa
    ServerAliveInterval 120

# ----- Connection to your VM via the Jumphost -----
Host {A_Friendly_Name_For_Your_VM}
    HostName {10.57.XXX.XXX} # The Floating IP of your VM
    User {ubuntu} # or rocky, etc.
    IdentityFile {/path/to/your/private_key}
    ProxyJump denbi-jumphost-01.bihealth.org
```

You can now connect directly to your VM from your terminal with:

```console
ssh {A_Friendly_Name_For_Your_VM}
```

      
## Storage Management

### Creating and Attaching Volumes


Use volumes to add more persistent disk space to a VM. A volume can only be attached to one VM at a time but will persist even after the VM is deleted.

**Warning:** Creating a volume larger than 250 GB may cause snapshot operations to be slow or to fail.

1. Create the Volume
- Navigate to Project -> Volumes -> Volumes.

- Click "Create Volume", give it a name, and set the desired size.

2. Attach the Volume to a VM
- Find the newly created volume in the list.

- Click the dropdown arrow on the right and select "Manage Attachments" (or "Attach Volume").

- Select the VM you want to attach it to and click "Attach Volume".

3. Format and Mount the Volume on the VM

After attaching the volume, you must format (only for new volumes) and mount it inside the VM.

- Create a filesystem (run this command only once for a new volume):


```console
sudo mkfs.ext4 /dev/vdb
```

- Mount the volume:

```console
# Create a mount point (if it doesn't exist)
sudo mkdir -p /mnt/data

# Mount the volume
sudo mount /dev/vdb /mnt/data
```

### Creating an NFS Share
NFS shares are ideal for storing large amounts of data that need to be accessed by multiple VMs within your project.

1. Create the Share
- Navigate to the Shares section and click **"Create Share"**.

- Fill in the details:

  - Share Name: A descriptive name.

  - Share Protocol: NFS (pre-selected).

  - Size (GiB): The size of the share (must be within your project's quota).

  - Share Type: isilon-denbi.

  - Availability Zone: nova.

2. Manage Access Rules
By default, a new share is inaccessible. You must grant access to your VMs.

- Find your share, click the dropdown arrow, and select **"Manage Rules"**.

- Click **"Add Rule"** and provide the following:

  - Access Type: ip.

  - Access Level: read-write or read-only.

  - Access To: The IP address of the VM you want to grant access to.

**Important:** Keep your access rules updated to ensure only authorized VMs can access your data.

  
### Mount the Share on Your VM
1. **Find the share path:** In the Shares dashboard, click on your share's name. The path will be listed under "Export locations". It will look like this:

```console
manila-prod.isi.denbi.bihealth.org:/ifs/denbi/prod/$yourShareUiid.
``` 

2. Install the NFS client (if not already installed):


```console
# For Ubuntu/Debian
sudo apt update && sudo apt install nfs-common
```

3. Mount the share:

```console
sudo mount -t nfs your-full-export-location-path /path/to/mount/point
# Example:
sudo mount -t nfs manila-prod.isi.denbi.bihealth.org:/ifs/denbi/prod/share-YOUR_UIID /mnt/volume
```

4. Set permissions: Ensure the correct user owns the mounted directory.

```console
# Example for an Ubuntu VM:
sudo chown ubuntu:ubuntu /mnt/volume
```

**Important:** At present, only NFS version 3 is supported.

The following should be set to the local NFSv4 domain name

```console
cat /etc/idmapd.conf 
[General]
#Verbosity = 0
# The following should be set to the local NFSv4 domain name
# The default is the host's DNS domain name.
Domain = denbi.bihealth.org
```

## Using the OpenStack API

This guide shows how to set up the openstack-cli client on a VM (tested on Ubuntu 22.04) to manage your project from the command line.

1. Create Application Credentials: In the OpenStack dashboard, go to your user menu (top right), click "Application Credentials", and create a new credential.

![select application credentials](img/berlin/application_credentials_select.png)

![create application credentials](img/berlin/application_credentials_create.png)

2. Download Files: Download the two files provided: `openrc.sh` and `clouds.yaml`.

![download application credentials files](img/berlin/application_credentials_files.png)

3. Launch a VM and copy both files to it.
4. Move clouds.yaml: Place the clouds.yaml file in the correct directory:
```console
mkdir -p ~/.config/openstack/
~/.config/openstack/
```

5. Install virtualenv:

```bash
sudo apt-get update
sudo apt-get install python3-virtualenv
```
6. Create and activate a virtual environment:.
```bash
virtualenv ~/venv
source ~/venv/bin/activate
```
7. Install the OpenStack client:

```bash
pip install python-openstackclient
```
8. Load the credentials:
```bash
source openrc.sh
```
9. Test the CLI:
```bash
openstack server list
```

### Using the OpenStack API from Your Local Machine

1. Set up a SOCKS proxy: First, configure your `~/.ssh/config` to create a SOCKS proxy when you connect to the jumphost. Add this entry to your local ~/.`ssh/config` file:

```bash
Host de.NBI-SOCKS-Proxy
    HostName denbi-jumphost-01.bihealth.org
    User {Your_LifeScience_Login}
    IdentityFile {/path/to/your/private_key}
    DynamicForward localhost:7777 # you can choose another port here
    ServerAliveInterval 120
```
Now, open a terminal and run 

```bash
ssh de.NBI-SOCKS-Proxy
```

2. Configure your environment: In a new terminal, export the following environment variables to direct API traffic through the prox
```bash
export http_proxy=socks5h://localhost:7777
export https_proxy=socks5h://localhost:7777
export no_proxy=localhost,127.0.0.1,::1
```

You should now be able to run OpenStack CLI commands from your local machine, provided you have also configured it with your credentials (`clouds.yaml` and `openrc.sh`)

## Adding multiple SSH-Keys
To grant access to multiple users when you first create a VM, use a customization script.

1. During VM launch, go to the Configuration tab.


2. In the Customization Script text box, enter the public keys in the following cloud-config format:

```bash
    #cloud-config
    ssh_authorized_keys:
        - Full public ssh-key of User-1
        - Full public ssh-key of User-2
```
Both User 1 and User 2 will have access to the VM after it boots.


## Uploading Custom Linux Images

If you need an OS that we do not provide, you can upload your own.

1. Navigate to Project -> Compute -> Images.

2. Click "Create Image".

3. rovide an Image Name and select the File to upload.

4. Set the Format (usually QCOW2 - QEMU Emulator).

5. If required, specify the minimum disk and RAM requirements for the image.

Once uploaded, the image will be available for use only by members of your project.

