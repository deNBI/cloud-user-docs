# de.NBI Cloud Tübingen
Welcome to the de.NBI Cloud site Tübingen. In the following we will
give you a basic introduction how to use our cloud site.

## General concept of the de.NBI Cloud Tübingen
A cloud like the one you will use here can be seen as computing resources which are available on demand.
You can get much more compute cores (CPU), main memory (RAM) and also storage capacity than you have
available on your own work station. The de.NBI Cloud Tübingen provides you the mentioned resources as an infrastructure (IaaS).
The available resources are used by starting Virtual Machines (VMs) on the provided computing machines.
You can start different virtual machines with different Linux based operating systems (OS) which consume different kind of
resources. The VMs can be customized on your own to fit your needs in the best way.
What you get is a computing infrastructure where you can run calculations or simulations with a flexible amount of resources
in your own computing environment (VM).

## Login
You need to apply for a login for https://denbi.uni-tuebingen.de. While the overall de.NBI cloud is still being build, the central application mechanisms are not available yet.
For the time being, get in touch with us (jens.krueger@uni-tuebingen.de, maximilian.hanussek@uni-tuebingen.de).

Please note, you are responsible for everything that happens with the virtual machines (VMs) you deploy! We as resource provider are not liable for anything and do not give any guarantees. It is anticipated to have a more sophisticated user agreement available till the end of 2017.

## Operating Systems
Here, we are talking about the operating system of your notebook or workstation, not the one of the VM. If you are a Linux User, we assume that you know what you are doing. If you are using MacOS you are hopefully aware that it is based on BSD and therefore very similar to other Linux distributions.

For a normal Windows user, we suggest using Putty (http://www.putty.org/) to access the deployed VMs. It comes with ‘puttygen’ which should be used to generate your SSH Keys.

## SSH-Keys
To access your VMs, a valid SSH key pair is required. On all UNIX based operating systems ‘keygen’ may be used to create a key pair. A Linux command example is given below:

<pre>ssh-keygen –t rsa</pre>

Please note, keep your private key as private as you would do it with your credit card PIN number. We will never ask you to share your private key.

### Generating SSH Key Pair (Windows)
Start ‘puttygen’ and click on generate. You need to move your mouse cursor above the grey field to create enough entropy. Enter a passphrase, twice. Save your private and public key into separate files e.g, bla.ppk and bla.key.

### Deploying a Key Pair
Login to the Horizon dashboard https://denbi.uni-tuebingen.de and navigate to Key Pairs via Project / Compute. Click on ‘Import Key Pair’ and insert your public key after giving it a name.

## Launching an Instance
Navigate to Instances via Project / Compute and click on Launch Instance (upper right). The following entries for the VM are only examples, please chose the appropriate settings for your work case (Operating System (Images), Resources (Flavors)).

#### Details
<pre>Instance Name: <some name you like>
Availability Zone: Nova
Count: 1</pre>

#### Source
<pre>Select Boot Source: Instance Snapshot or Images
Create New Volume: No (Otherwise launching the instance will fail !)
Allocated: Select the required OS by clicking on the up arrow</pre>

#### Flavor
<pre>Allocated: Select the required flavor by clicking on the up arrow</pre>

#### Networks
<pre>Allocated: Select the set up network by clicking on the up arrow beneath the network name</pre>

#### Network Ports
<pre>Leave it unchanged</pre>

#### Security Groups
<pre>Allocated: Select the set up network by clicking on the up arrow beneath the network name and move ‘default’ to the Available section</pre>

#### Key Pair
<pre>Select your key pair</pre>

#### Configuration
<pre>Leave it unchanged</pre>

#### Server Groups
<pre>Leave it unchanged</pre>

#### Scheduler Hints
<pre>Leave it unchanged</pre>

#### Metadata
<pre>Leave it unchanged</pre>

Finally launch the instance. You should see a fresh instance entry. It may take a couple of minutes to spawn the instance depending on the requested resources. 

## Accessing a VM
For Linux and MacOS just use ssh, specifying the correct IP, the right key and the username of the OS you have chosen for example ‘centos’. For Windows, start ‘Putty’ and enter the IP address of your VM under Hostname (or IP address). It can be found within the Horizon dashboard under Instances. An example of a Linux command is given below:
<pre>ssh –i /path/to/private/key <osname>@<IP-Address></pre>

An example for a centos machine with the IP 1.2.3.4 would be:

<pre>ssh –i /path/to/private/key centos@1.2.3.4</pre>

If you need x-forwarding for graphical user interfaces don’t forget to set the –X flag and check if the xauth package is installed on the host and the server and the x-forwarding settings are correct. For Windows user we suggest to use xming (https://sourceforge.net/projects/xming/). 

For Windows using Putty you have to navigate in Putty to Connection / Data and enter ‘centos’ as Auto-login username. The user name may be different for different Boot Sources, but here we have a CentOS based image. Under Connection / SSH / Auth select the file containing your private key matching the public one you have used during the creation of your VM. Enable X11 forwarding under Connection / SSH / X11. Go back to Session and save the settings for later reuse.
Click on Open to connect to your VM via SSH. When connecting for the first time a warning related to server host keys may appear. Confirm with yes. Enter the passphrase you have set during the creation of your key pair.
You now should have a prompt on your VM.
Please note, each time you are shutting down and deleting the VM or redeploy the VM the IP address will change. So first check if you have the correct IP address if problems occur. If are just logging out of the VM via the exit command, the IP address will not change.

## Transferring data
Per default you will have a varying amount of space available (root disc) within your VM depending on the chosen operating system. More is easily available through Swift or Cinder volumes. How to use Cinder Volumes is explained below. Further you can use a flavor with 20GB of root disc space to enlarge the available default space.
You may copy data from and to your VM using simply the Linux  scp  command with the –i flag to use your SSH key. For Windows users, the usage of WinSCP (https://sourceforge.net/projects/winscp/) is suggested. Of course, the correct IP, the right key and the username ‘centos’ for example has to be specified.

## Using Cinder Volumes
Cinder Volumes are nothing else than block devices like a hard drive connected to your computer but in this case virtual. You can mount format and unmount it like a normal block device. In the following it is explained how to create a Cinder Volume and how to use it in your VM. But before some remaks. It is only possible to attach a Cinder Volume to exactly one VM. So you can not share one Volume with other VMs. A more cheerful remark is that the data saved on a Cinder Volume is persistent. As long you do not delete the Volume in the Dashboard (Horizon) your data will not get lost by deleting the VM or anything else happening with the VM.  

In the Dashboard (Horizon) you will navigate to the `Compute` section and then to the `Volume` section.
Here you can create a new volume entering the following parameters
<pre>Volume name: Type in any name you want to
Description: Describe for which purpose you will use the volume (optional) 
Volume Source: Set it to `No source, empty Volume` to get an empty block device
Type: quobyte_hdd
Size (GiB): Select the desired size in Gigabytes
Availability zone: nova</pre>

Then click `create volume` and your volume will appear in the list of volumes with the status `Available`.
Now you have to attach the just created volume to your VM. This is done by changing to the `instance` section under the `compute` section and clicking on the arrow on the right side belonging to your VM. Choose `Attach Volume` and choose the just created volume. Now your volume is connected to your VM like if connect a hard drive via USB with your computer.
Now you have to login into your VM, format and mount the volume.
You will find your volume with the command
<pre>lsblk</pre>
This command will list all your block devices connected to your VM.
Chose the correct device (mostly the name will be the second entry, you can orientate oneself on the SIZE parameter) and format it with a filesystem if you are using this volume for the first time. Common filesystems are ext4 or xfs.
<pre>mkfs.ext4 /dev/device_name</pre>

After the formating you have to create a mountpoint
<pre>mkdir -p /mnt/volume</pre>

Check that you have the correct permissions for this directory, otherwise set them with the follwoing command
<pre>chmod 777 /mnt/volume/</pre>

And mount the Cinder Volume under the created directory
<pre>mount /dev/device_name /mnt/volume</pre>

Now you should see your device by executing the command
<pre>df -h</pre>

If you do not need you Cinder Volume you can also unmount it with
<pre>umount /dev/device_name</pre>

## Resize a Cinder Volume
If you find out that you need more space for your Cinder volume and want to increase the volume size, you can do this over the dashboard. Go to the Volumes section on the left side. If the Cinder volume is already attached to a VM please unmount the Cinder volume in the VM and detach it over the dashboard. Only if the Cinder volume is detached you can increase the size. Now choose the “Extend Volume” button after you have clicked on the down showing arrow on the right of the Cinder volume you want to extend. Enter the new size (in Gigabytes) and click on the button “Extend Volume”.
After this procedure has finished successfully you can attach the extended Cinder volume to your VM. Depending on which filesystem you use on your Cinder volume there are different procedures necessary to make the new capacity available.
For an xfs formatted filesystem:
Mount the volume as usual and run the following command
<pre>sudo xfs_grow -d MOUNTPOINT</pre>
If you followed the instructions above the `MOUNTPOINT` would be `/mnt/volume` After that you can use the extend volume with the new capacity.

For an ext4 formatted filesystem:
Do not mount the volume. If you can see it with the lsblk command that is enough. Run the following command to get increase the capacity
<pre>sudo resize2fs /dev/device_name</pre>
The `/dev/device_name` is the same you have used in the mount command above.
Now you can mount and use it as usual and also use the extended capacity.

If you use another filesystem than xfs or ext4 please look up if and how an increase of the capacity is possible.

## Attach a second interface
If you need a second interface for example to use direct volume mounts of our Quobyte storage for handling sensitive data or you need an internal network to build a virtual cluster where the compute nodes usually do not need to be accessed by the outside network this guide will help you to get them configured.
In the following we will differentiate between VM images based on CentOS7 and Ubuntu 18.04. (Bionic).

### CentOS7
1. First launch a VM with a publicly acessible IP address, as usual
2. Login to the VM
3. Change to the root user 
<pre>sudo su -</pre>
4. The following command will set the default gateway to network interface eth0 which should be the interface for the public IP address:
<pre>echo 'GATEWAY=eth0' >> /etc/sysconfig/network</pre>
5. Exit as root user running the following command:
<pre>exit</pre>
6. Attach a second interface of your choice via the webinterface (OpenStack Dashboard)
7. Change back to the VM and run the following command to configure the second interface:
<pre>sudo dhclient</pre>
8. Check if the interface eth1 (usually) now has an IP address configured matching the one shown in the webinterface with the following command:
<pre>ip a</pre>
You should see something similar to this output (XXX are replaced by numbers or letter)
<pre>1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host 
       valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
    link/ether fa:16:3e:16:91:XX brd ff:ff:ff:ff:ff:ff
    inet 193.196.20.XXX/XX brd 193.196.20.XXX scope global dynamic eth0
       valid_lft 85038sec preferred_lft 85038sec
    inet6 fe80::f816:3eff:fe16:91XX/64 scope link 
       valid_lft forever preferred_lft forever
3: eth1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
    link/ether fa:16:3e:4b:83:XX brd ff:ff:ff:ff:ff:ff
    inet 192.168.58.XXX/XX brd 192.168.XX.255 scope global dynamic eth1
       valid_lft 85040sec preferred_lft 85040sec
    inet6 fe80::f816:3eff:fe4b:83XX/64 scope link 
       valid_lft forever preferred_lft forever</pre>

The configuration of the network will not be persistent and after a reboot it would be gone. If you want to make this configuration persistent,
please follow the following steps we are assuming here that the second interface name is eth1. Further you can skip steps 7. and 8. from above:
9. Change to the root user 
<pre>sudo su -</pre>
10. Create a new network config file
<pre>vi /etc/sysconfig/network-scripts/ifcfg-eth1</pre>
With the following content:
<pre>DEVICE=eth1
NAME=eth1
BOOTPROTO=dhcp
NM_CONTROLLED=no
PERSISTENT_DHCLIENT=1
ONBOOT=yes
TYPE=Ethernet</pre>
Save and close the file with `:wq` 
11. Bring the interface up by running the following command:
<pre>ifup eth1</pre>
Wait until the additional interface has been configured.

12. Check if the interface has been configured correctly running the command:
<pre>ip a</pre>
which should print out a similar output as shown above.

13. Exit as root user running the following command:
<pre>exit</pre>


### Ubuntu 18.04. (Bionic)
1. First launch a VM with a publicly acessible IP address, as usual

2. Attach a second interface of your choice via the webinterface (OpenStack Dashboard)

3. Check the interface name of the second interface, usually it should be 'ens6' with the following command:
<pre>ip a</pre>

4. Change to the root user 
<pre>sudo su -</pre>

5. Create a new network config file
<pre>vi /etc/systemd/network/ens6.network</pre>
With the following content:
<pre>[Match]
Name=ens6

[Network]
DHCP=ipv4

[DHCP]
UseMTU=true
RouteMetric=200</pre>
Save and close the file with `:wq`

5. Restart the network with the follwoing command:
<pre>systemctl restart systemd-networkd</pre>

6. Check if the interface has been configured correctly running the command:
<pre>ip a</pre>
which should print out a similar output as shown above for the centos7 section.
The made changes here are directly persistent.
