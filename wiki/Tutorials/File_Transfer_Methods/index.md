# File Transfer from/to de.NBI Cloud
At some point you want to use your own data in the de.NBI Cloud or you would like to copy the results from your cloud computation to your local device. Here we present different ways to copy data from or to the de.NBI Cloud. This tutorial is meant for users of the simplified cloud access portal SimpleVM. In SimpleVM a connection to the VM is made via an IP-Adress and a Portnumber. Therefore your have to always specify the port number which is used to connect to the VM. de.NBI Cloud users which access their VMs via OpenStack directly connect to the default SSH port 22 which can be omitted.

## Different tools for different use cases
There are different tools for copying files from/to the de.NBI Cloud each for different use cases. Under Linux you can choose between different comman line tools. Some of them can also be used with a graphical user interface (GUI) by using a file manager. For Windows users it may be best to use a GUI tool like [WinSCP](https://winscp.net/eng/index.php). This tutorial will cover the following Linux tools:

1. [scp](#SCP) -- secure copy (remote file copy program)
2. [sshfs](#SSHFS) -- filesystem client based on ssh 
3. [rsync](#Rsync) -- a fast, versatile, remote (and local) file-copying tool 

## <a name="SCP"></a> 1. SCP -- secure copy (remote file copy program)
Secure Copy (SCP) is, as you already guessed, a command line tool for copying files from/to remote devices. It is based on the Secure Shell (SSH), which you already used to connect to your virtual machine. SCP will establish a connection to the remote machine, transfer the file(s) and close the connection afterwards. If you want to transfer more files you have to start SCP again.

### Installation
Remote machine:
The Virtual Machine in the Cloud should already have SCP installed.

Local Machine:
Linux shippes SSH with SCP by default.

### Usage
The usage is quite simple. To copy a file TO the remote machine use:

```
scp -i <id-file> -P <port> <file> <user>@<IP>:<path>
```

Example:
This will connect to server ``111.222.333.444`` at port ``30000`` using the public key ``mykeyfile`` and will copy the local file ``data.csv`` from your local working directory to the remote machine as ``analysis/input/data.csv``.

```
scp -i mykeyfile -P 30000 data.csv ubuntu@111.222.333.444:analysis/input/data.csv
```

To copy a file FROM the remote machine use:

```
scp -i <id-file> -P <port> <user>@<IP>:<path> <file>
```

Example:
This will connect to server ``111.222.333.444`` at port ``30000`` using the public key ``mykeyfile``and will copy the remote file ``analysis/input/data.csv`` to your local working directory as file ``data.csv``.

```
scp -i mykeyfile -P 30000 ubuntu@111.222.333.444:analysis/input/data.csv data.csv 
```

## <a name="SSHFS"></a> 2. SSHFS -- filesystem client based on ssh 
SSHFS allows to mount a remote file system like a normal file system. The benefits of using SSHFS is that the file 
system remains available as long it is mounted. Furthermore, as the remote file system is mounted like a normal local 
file system, you can work on remote files like you work with local files by using default file access and transfer tools 
like ``ls``, ``cp`` and ``mv``. You basically don't have to think about if a file is on a remote or on a local machine. 
Furthermore modern graphical file managers like Nautilus, Thunar etc. recognize the mounted file system so you can access 
the remote file system with the graphical file manager.

!!! note
    Files mounted with SSHFS are accessed through the internet. Therefore reading and writing can at most be as fast as 
    the network speed, which in most cases is too slow. We strongly advise against using SSHFS as an external harddrive 
    or volume alternative. Instead we advise to create and attach a volume to your remote server (via the portal if you have 
    SimpleVM project or the openstack dashboard if you have an Openstack project) and transfer your files with scp, rsync 
    or another suitable method.

### Installation
Install SSHFS on your local machine and mount the remote file system of the virtual machine on the local machine. 
This requires permission to install software and to mount file systems on the user level on your local machine.

On an Ubuntu system SSHFS is installed via:

```
sudo apt install sshfs
```

### Usage
First we need to install SSHFS on the local machine.

We create a directory as a mount point from which the mounted file system will be available. You can choose any 
direcotry name, but here we call it ``remotefs``. Our working directory in this case is ``/home/ubuntu/``.

```
mkdir remotefs
```

Now we can mount the remote file system with SSHFS. The general command looks lie this:

```
sshfs <user>@<hostname>:</absolute/path/to/remote/directory> <mountpoint> -o IdentityFile=</absolute/path/to/identity_file> -p <portnumber>
```

Let's try a real world example: You want to access a remote data directory ``/home/ubuntu/analysis`` by mounting it 
in the local directory ``/home/ubuntu/remotefs``. 

```
sshfs ubuntu@<IP>:/home/ubuntu/analysis remotefs -p <PORT> ``-o IdentityFile=/home/ubuntu/mykeyfile``
```
where ``<IP>`` the IP of the gateway machine and ``<PORT>`` is the PORT opened for your virtual machine. If you are a 
SimpleVM user you may find this information on ``How to connect`` of your virtual machine on the instance overview.

In case you allowed connecting with a public/private key you have to provide the public key with 
``-o IdentityFile=/home/ubuntu/mykeyfile``. It is important to give the absolute path to the public key file.

To unmount the mounted file system use this command

```
fusermount -u <mountpoint>
```

Hint: If you mounted the remote file system in a subdirectory like ``subdir/remotefs`` you have to give the same path 
to fusermount to unmount it (e.g. ``fusermount -u subdir/remotefs``).


### <a name="Rsync"></a> 3. RSYNC -- a fast, versatile, remote (and local) file-copying tool 
Rsync allows synchronization of two directories, e.g. a local and a remote directory. It checks for the differences between the directories and only transfers the differences which speeds up the file transfer a lot. Furthermore, the data can be compressed before transfer, to speed up the transfer. This feature renders Rsync perfect for frequent file transfers of large directories or backup purposes. Rsync offers a large number of options as it is a very powerfull tool. Here we only describe the basics for a very simple file transfer between a local and a remote machine. Please see the manual page for a complete list of options (``man rsync``).

#### Installation
Rsync is installed by default on most Linux systems.

#### Usage
Rsync has to be installed on the local and the remote machine in order to work. To avoid confusion all commands are entered on the local machine.
To copy the content of a local directory to a remote directory in the de.NBI Cloud via Rsync using SSH use this command:

```
rsync -avu --progress -e "ssh -i mykeyfile -p <port>" /local/dir1/ <user>@<IP>:/remote/dir2/ 
```

The trailing slash (``/``) at the end of ``dir1`` tells Rsync to copy the content of ``dir1`` to ``dir2`` without creating ``dir1`` inside of ``dir2``. In case you want to create ``dir1`` with all its content inside ``dir2`` remove the trailing slash behind ``dir1`` (so it will look like this: ``/local/dir1``).

The parameters used are:

``-a`` Archive mode: Copies files recursively and preserves users, groups, symbolic links, file permissions, and timestamps. ``-v`` gives a more detailed output. ``-u`` skip files that are newer on the receiver. ``--progress`` show file transfer progress. ``-e "ssh -i mykeyfile -p <port>"`` tell rsync to connect via SSH using the keyfile and port belonging to the virtual machine you want to connect to.

To copy data from a virtual machine in the de.NBI cloud to a local machine use:

```
rsync -avu --progress -e "ssh -i mykeyfile -p <port>" <user>@<IP>:/remote/dir1/ /local/dir2/
```

In some cases Rsync is not installed in the default installation path. In this case you have to tell where Rsync is installed on the remote machine with ``--rsync-path=/path/to/rsync``. 
By default Rsync will delete files on the receiver side before any files are transfered. Rsync has very delicate options to delete files under different circumstances which cannot be covered in this tutorial. In case you are unsure what data will be transfered and/or deleted  you can start a trial run with the option ``--dry-run``. For detailed information consult the rsync manual page by typing ``man rsync``.

