# File Transfer from/to de.NBI Cloud
At some point you want to use your own data in the de.NBI Cloud or you would like to copy the results from your cloud computation to your local device. Here we present different ways to copy data from or to the de.NBI Cloud.

## Different tools for different use cases
There are different tools for copying files from/to the de.NBI Cloud each for different use cases. Under Linux you can choose between different comman line tools. Some of them can also be used with a graphical user interface (GUI) by using a file manager. For Windows users it may be best to use a GUI tool like [WinSCP]https://winscp.net/eng/index.php . This tutorial will cover the following Linux tools:

* scp
* sshfs
* rsync

## SCP
Secure Copy (SCP) is, as you already guessed, a command line tool for copying files from/to remote devices. It is based on the Secure Shell (SSH), which you already used to connect to your virtual machine. SCP will establish a connection to the remote machine, transfer the file(s) and close the connection afterwards. If you want to transfer more files you have to start SCP again.

### Installation
Remote machine:
The Virtual Machine in the Cloud should already have SCP installed.

Local Machine:
Linux shippes SSH with SCP by default.

### Usage
The usage is quite simple. To copy a file TO the remote machine use:

  scp -i <id-file> -P <port> <file> <user>@<IP>:<path>

Example:
This will connect to server 111.222.333.444 at port 30000 and will copy the local file data.csv from your local working directory  to the remote machine as analysis/input/data.csv

  scp -i mykeyfile -P 30000 data.csv ubuntu@111.222.333.444:analysis/input/data.csv

To copy a file FROM the remote machine use:

  scp -i <id-file> -P <port> <user>@<IP>:<path> <file>

Example:
This will connect to server 111.222.333.444 at port 30000 and will copy the remote file analysis/input/data.csv to your local working directory as file data.csv

  scp -i mykeyfile -P 30000 ubuntu@111.222.333.444:analysis/input/data.csv data.csv 


## SSHFS
SSHFS allows to mount a remote file system like a normal file system. The benefits of using SSHFS is that the file system remains available as long it is mounted. Furthermore, as the remote file system is mounted like a normal local file system, you can work on remote files like you work with local files by using default file access and transfer tools like ls, cp and mv. You basically don't have to think about if a file is on a remote or on a local machine. Furthermore modern graphical file managers like Nautilus, Thunar etc. recognize the mounted file system so you can access the remote file system with the graphical file manager.

### Installation
There are two ways to use SSHFS:

Option 1: Install SSHFS on your local machine and mount the remote file system of the virtual machine on the local machine. This requires permission to install software and to mount file systems on the user level on your local machine. 

Option 2: Install SSHFS in the remote virtual machine in the Cloud and mount the file system from the local machine in the remote virtual machine. This option allows the benefits of using SSHFS on local machines which do not allow the installation of software or mounting of file systems. We will focus on this option in this tutorial.

### Usage
First we need to install SSHFS on the remote virtual machine

  sudo apt install sshfs

We create a directory as a mount point from which the mounted file system will be available. You can choose any direcotry name, but here we call it remotefs.

  mkdir remotefs

Now we can mount the remote file system with SSHFS. The general command looks lie this:

sshfs <user>@<hostname>:</absolute/path/to/remote/directory> <mountpoint> -o IdentityFile=</absolute/path/to/identity_file> -p <portnumber>

Let's try a real world example: You want to access your local data directory /home/localuser/analysis by mounting it in the remote virtual machine in the directory /home/ubuntu/analysis . 

  sshfs user@111.222.333.444:/home/user/analysis remotefs -p 30000

In this case sshfs will ask for local-user's password. In case you allowed connecting with a public/private key you have to provide the public key with -o IdentityFile=/home/ubuntu/mykeyfile . It is important to give the absolute path to the public key file.

To unmount the mounted file system use this command

  fusermount -u <mountpoint>

Hint: If you mounted the remote file system in a subdirectory like subdir/remotefs you have to give the same path to fusermount to unmount it (e.g. fusermount -u subdir/remotefs )


### RSYNC
Rsync allows synchronization of a local and a remote directory. It's a very powerfull tool 
incremental synchronization between remote and local folders

