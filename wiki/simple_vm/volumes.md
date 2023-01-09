# Volumes

Volumes offer extra disk space for your virtual machine.
You can create new volumes on the volume overview page or when starting a new virtual machine. 
You can attach and detach volumes on the volume overview or on the instance overview, or their detail page.

## Layout

![general](./img/volumes/general.png)

### 1. Create and attach a volume

Create and attach a new volume. For more information, see [Create a volume](#create-a-volume).

### 2. Pagination

Set how many volumes you want to see on a page and scroll through the pages.

### 3. Filter volumes

Filter the list of volumes.<br>
Filter by volume name, OpenStack ID of a volume, project name and virtual machine name.

### 4. Action on multiple volumes

Perform an action on all selected volumes.<br>
`Select all` for all volumes or `select` specific volumes.

### 5. Volume information

- The project it belongs to.
- The attached vm. Click to get to the [detail page](instance_detail.md) of the vm.
- The name of the volume.
- The status of the volume.
- The storage size of the volume.

### 6. Action on one volume

![actions](./img/volumes/actions.png)

Perform an action on one volume.

* Attach volume<br>
  Attach an available volume to an existing virtual machine.
* Detach volume<br> 
  Detach an in-use volume from an existing virtual machine.
* Extend volume<br> 
  Extend the size of the volume if your project has enough resources left. 
  You usually have to configure the volume on the virtual machine after extending it.
  For more information, see [Extend a volume](#extend-a-volume).
* Delete volume: deletes the volume and all its data.

!!! info "Attaching and detaching"
    You can attach and detach volumes to and from an active virtual machine.

## Create a volume

You have two ways to create a volume:

1. When you crate a vm, you can create a [New volume](new_instance.md#new-volume). 
   The volume gets automatically mounted this way.
2. At the Volume tab choose to create a volume.

![create_volume](./img/volumes/create_and_attach.png)

To use the new volume, you need to create a filesystem and mount it. See [mount a volume](#mount-a-volume).

### Create the volume file system

???+ warning "Do that only once"
    Read carefully. Do this step only once after you created your volume by using the `Create & Attach volume`
    dialog. Repeating this step can destroy all the data on your volume.

To place files onto your new volume, there needs to be a file system on it.
To generate a file system, you need to "format the device".<br>
First, use this command to list all the block devices connected to your VM:

```shell
lsblk -o NAME,SIZE,MOUNTPOINT,FSTYPE,TYPE | egrep -v "^loop"
```

You get a list like this:

| NAME    |  SIZE | MOUNTPOINT | FSTYPE | TYPE |
|:--------|------:|:-----------|:-------|:----:|
| vda     |   50G |            |        | disk |
| └─vda1  | 49.9G | /          | ext4   | part |
| └─vda14 |    4M |            |        | part |
| └─vda15 |  106M | /boot/efi  | vfat   | part |
| vdb     |   50G | /mnt       | ext4   | disk |
| vdc     |    1G | [SWAP]     | swap   | disk |
| vdd     |  300G | /vol/data  | ext4   | disk |
| vde     |  500G |            |        | disk |

You get shown the name, the size, the mountpoint, and the file system type from all connected block devices.

???+ tip "What do the columns tell?"
    The column `NAME` tells you the name of the block device. When you perform an action on it, you typically
    prepend `/dev`. For example, to unmount the volume vdd, you use `sudo umount /dev/vdd`.
    Parts of one disk have a number at the end. See the column `TYPE`.<br>
    The column `SIZE` tells you the size of the block device in human-readable format `M`, `G`, `T`, and so on.<br>
    The column `MOUNTPOINT` tells you where you find the data from that block device. When empty, you need to
    mount the device.<br>
    The column `FSTYPE` tells you the file system type of the block device. Many file system types exist.
    If you want to use a block device, but the fstype is empty, you need to format it.

???+ info "What devices does the output show?"
    One block device, usually vda, is your root disk. It has your operating system and all relevant files. 
    You can identify it by its mountpoint `/`. You must not alter the block device containing your root disk,
    you may damage your virtual machine irreversibly.
    Only alter it if you know what you do.<br>
    One block device, identified by fstype `swap`, is your swap disk or swap file.<br>
    One block device can show up at the mountpoint `/mnt`. This is typically the ephemeral disk, which shows only
    when you start a flavor with an ephemeral.<br>
    You can identify the volumes created, attached, and mounted when creating a vm, by comparing the size
    and mountpoint of the block device. Further, it shows the fstype `ext4`.

The volume you look for has an empty `FSTYPE`, an empty `MOUNTPOINT` and the `SIZE` should compare to the size of 
the volume you created and attached. The size can differ a bit because of differences in Bit and Byte.<br>
In the table from the example output, the device you look for would be vde.

!!! Danger "Formatting a device `DESTROYS ALL DATA` on it!"
    You must format new data disks, for example volumes, **only once** to use them.<br>
    **NEVER** apply this command to an **ALREADY FORMATTED DISK** if you value the data on that disk.<br>
    See if a volume has a file system type by using the `lsblk` command.

Format the volume with a filesystem, e.g. `ext4` or `xfs`:

```shell
mkfs.ext4 /dev/vdx
```

## Mount a volume

When you mount a volume, you make its data available under a path.
You can call this path a mountpoint or mount path.<br>
Create a mountpoint with:

```shell
sudo mkdir -p /vol/RENAME_ME
```

Change `RENAME_ME` to a path where you want your volume data accessible, for example to `/vol/data`.

To get an overview of all connected devices and get the `device_name`, use:

```shell
lsblk -o NAME,SIZE,MOUNTPOINT,FSTYPE,TYPE | egrep -v "^loop"
```

Mount the volume under the created directory with:

```shell
sudo mount /dev/device_name /vol/RENAME_ME
```

Change the owner of the volume data with:

```shell
sudo chown -R ubuntu:ubuntu /vol/RENAME_ME
```

Use again the lsblk command to verify the changed mountpoint.

```shell
lsblk -o NAME,SIZE,MOUNTPOINT,FSTYPE,TYPE | egrep -v "^loop"
```

If you don't need the volume you can unmount it with:

```shell
umount /dev/device_name
```

### After a vm restart

When you reboot your vm, or stop and resume it, you might need to mount your volumes again.<br>
You can change the `/etc/fstab` file to automatically mount volumes at startup.
Get the devices connected to your vm with:

```shell
lsblk -o NAME,SIZE,MOUNTPOINT,FSTYPE,TYPE,UUID | egrep -v "^loop"
```

A device doesn't get attached under the same name every time, therefore, use the UUID of a device.
Open `fstab` with:

```shell
sudo nano /etc/fstab
```

Add a line like:

```shell
UUID=uuid_of_your_volume	/vol/RENAME_ME	auto	defaults	0	2
```

Save and exit with ++ctrl+x++ and confirm when asked whether you want to save.
To mount the volume run:

```shell
sudo mount -a
```

That command mounts every volume in the fstab file.
Your volume gets mounted, every time you restart your vm, under `/vol/RENAME_ME`.

## Extend a volume

If you have a volume and want to increase the volume size, you can do this at the volume overview.

![extend_volume](./img/volumes/extend_volume.png)

!!! caution "Volume must be available"
    The volume has to have the status `available`.

After you extended your volume, attach the volume to your vm.
Depending on the filesystem you use on your volume, you need different procedures to make the new capacity available. 

###  XFS formatted filesystem

[Mount the volume](#mount-a-volume) and run:

```shell
sudo xfs_growfs -d <MOUNTPOINT>
```

Afterward, you can use the extended volume.

###  Ext4 formatted filesystem

Don't mount the volume. Get the `device_name` of your volume with:

```shell
lsblk -o NAME,SIZE,MOUNTPOINT,FSTYPE,TYPE | egrep -v "^loop"
```

To increase the volume capacity, run:

```shell
sudo resize2fs /dev/device_name
```

Now you can mount the volume.
