# Best practices for data backup
When a virtual machine is deleted, the data saved on the machine will be deleted too. As we can not guarantee that a 
virtual machine and therefore the data on the machine will be accessable at all times due to possible hardware or 
software errors, we collect some best practices for data backup here.

## Remote backup
Although it is a rare occurence, it is possible that even volumes and snapshots might vanish or get corrupted. Therefore 
the absolute best practice for backuping data is by copying it to a remote hard drive, disk or other storage solution 
which is not part of the de.NBI Cloud.  
You may find a tutorial on how to copy data from your machine to a local or remote storage 
[here](../Tutorials/File_Transfer_Methods/index.md).  
If you have access to an object storage, please refer to the documentation of your object storage.

## Backup with volumes
!!! info "How to attach/mount volumes"
    You may find more information on how to create, attach and mount volumes [here](./volumes.md).

Volumes are a great way to backup files as they persist independently of your virtual machines (i.e. a mounted volume 
will not be deleted if your virtual machine is deleted) and the size limit is only determined by your requested project 
volume storage. 
!!! info "When to backup with volumes"
    Backup data on a volume when you want to backup data often, backup data from different virtual machines or want 
    to restore data without booting a new virtual machine. Backups on a volume are also independend of the state of your 
    system, i.e. they are stored safely even if you accidentally corrupt your system. 

There are different ways to backup data on a volume:  

  * Backup manually.  
    Mount the volume to the virtual machine you want to backup data from and either copy it with 
    ```bash
    cp -a /path/to/files/to/backup /path/to/backupDirectory/on/mounted/volume
    ```
    or use a program like rsync to sync data between two directories.  
    Another good practice is to archive the files you want to backup, e.g.
    ```bash
    tar -zcf /path/to/backupDirectory/on/mounted/volume/backup.tgz /path/to/files/to/archive
    ```
  * Backup automatically.  
    Mount the volume to the virtual machine you want to backup data from and create a cron job to automatically transfer 
    files to your mounted backup directory, e.g.
    ```bash
    0 0 * * * cp -a /path/to/files/to/backup /path/to/backupDirectory/on/mounted/volume 
    ```
    or
    ```bash
    0 0 * * * tar -zcf /path/to/backupDirectory/on/mounted/volume/backup.tgz /path/to/files/to/archive
    ```
    This cron jobs will backup your files every day at midnight.  
    For a more detailed guide on how to create and use cron jobs, please refer to one of the many guides you may find 
    on the internet.  

To transfer the backuped data to another machine B you will need to mount the volume on the machine B (and detach and unmount 
it first if it is still attached to machine A).  

A drawback of volumes is that they may only be mounted to one virtual machine at a time, which means that you can not 
backup data of multiple machines in parallel on one volume. One way to remedy this is by setting the volume up as a 
NFSv4 Share. A guide on how to do this is out of the scope of this guide and may be found for example 
[here](https://help.ubuntu.com/community/SettingUpNFSHowTo).

## Backup with snapshots
!!! info "How to create and use snapshots"
    You may find more information on how to create and start snapshots [here](./snapshots.md).

Snapshots preserve the files on the root disk and the full state of your RAM and you may use a snapshot to boot a new virtual 
machine. Snapshots may only be created manually and can not be automated for users of a SimpleVM project.

!!! info "When to backup with snapshots"
    Backup data with a snapshot when you want to preserve the full state of your virtual machine (e.g. before deleting your 
    virtual machine) or want to boot up one or many virtual machine(s) with your data already present.
    
!!! danger "Drawbacks to consider"
    As a snapshot preserves the full state of your virtual machine, only snapshots up to a maximum of 256 GB RAM are supported!  
    Snapshots are only available when creating a new virtual machine, they are not suitable to restore data on a running 
    machine!  
    Data on ephemeral disks will not be saved, data on ephemeral disks will be lost when not saved on a different storage 
    solution, e.g. a volume!  
    Data on attached and mounted volumes will not be saved in a Snapshot, but are of course still available on your volume.
