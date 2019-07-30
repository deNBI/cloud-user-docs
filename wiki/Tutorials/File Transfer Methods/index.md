# File Transfer from/to de.NBI Cloud
At some point you want to use your own data in the de.NBI Cloud or you would like to copy the results from your cloud computation to your local device. Here we present different ways to copy data from or to the de.NBI Cloud.

## Different tools for different use cases
There are different tools for copying files from/to the de.NBI Cloud each for different use cases. This tutorial will cover the following tools:

* scp
* sshfs
* sftp
* rsync

## SCP
Secure Copy (SCP) is, as you already guessed, a command line tool for copying files from/to remote devices. It is based on the Secure Shell (SSH), which you probably already used to connect to your virtual machine.

## Installation
### Linux
Typically SCP is installed with SSH, which is installed by default by most distributions.

### Windows


## Usage
The usage is quite simple. To copy a file TO the remote machine use:

scp <file> <user>@<IP>:<path>

To copy a file FROM the remote machine use:

scp Benutzer@Host:Verzeichnis/Quelldatei.bsp Zieldatei.bsp





## sshfs
3.1 installation in deNBI Cloud
3.2 usage
connection1: sshfs installed remotely, local FS mounted on remote VM
connection2: sshfs installed locally, remote FS mounted on local machine

## sftp
4.1 installation
4.2 using sftp with a file browser (nautilus, winscp, ...)

## rsync
5.1 installation
5.2 usage


scp
command line tool for connection-wise copying of files

sshfs
mounts a remote filesystem locally to enable CLI and GUI access

mkdir mountpoint

mounting (absolute paths are required!)
sshfs user@hostname:/absolute/path/to/remote/directory mountpoint -o IdentityFile=/absolute/path/to/identity_file -p portnumber

unmounting (unmounting only works for full mountpoint (e.g. sshfs user@hostname:/dir relative/mountpoint -> mountpoint has path "relative/mountpoint" not only "mountpoint")
fusermount -u mountpoint



sftp
file access via secure FTP



rsync
incremental synchronization between remote and local folders

