#Theia IDE
Welcome to a short **de.NBI tutorial** concerning [Theia IDE](https://www.theia-ide.org). Theia IDE is an extensible platform that allows to work with a virtual machine in a simplified, IDE like manner. A web based IDE like Theia-IDE comes at least with the following features:

- Simplified access to the VM via a browser
- File Browser
- Desktop IDE features (like code highlighting, code completion)
- Integrated terminal application

![[Theia IDE in action/screenshot ]](images/screenshot.png)

The goal of this tutorial, is to setup a web IDE (Theia IDE in our case) on a virtual machine running in the de.NBI cloud. The setup can be done manually, provided as userdata during virtual machine startup and as ansible role.

The latter two points are based on other de.NBI cloud tutorials ([UserData](../UserData/index.md), [Ansible](../Ansible/index.md)). The tutorial was tested against Ubuntu 18.04 LTS but should work with slightly modifications on most modern cloud images.


## Configuration

The general build process is quite easy and is well described on the Theia-Ide page ["Build your own IDE"](https://www.theia-ide.org/docs/composing_applications).  Feel free to follow the step-by-step documentation to build your own shell script or go the easy way and use the prepared [shell script](web-ide.sh).

### Dependencies
Depending on your base system,  building Theia-IDE needs some additional packages installed.

#### Ubuntu 16.04/18.04 and Debian 9

-  python-minimal
-  make
-  g++

```bash
> sudo apt-get install -y python-minimal make g++
```

#### REHL 7 / CentOS 7

- python
- make
- gcc
- gcc-c++

```bash
> sudo yum install python make gcc gcc-c++
```

## Start service 
After a successful build, we can start the IDE. 

```bash
> yarn theia start ~ --hostname 127.0.0.1 --port 8080
```

In our example we set the workspace to '~' and bind the process to 127.0.0.1:8080.

!!! warning "Warning"
    It is always a bad idea to bind the IDE to an external network device, since there is no encryption (https) or authorization provided by Theia-IDE.




## Access Theia-IDE

Since we bind the process to a local network device, we have to start a ssh session with port tunneling enabled. The ssh command ...

```bash
                                 A         B                     C
                               ----- --------------        -------------
> ssh [-i your_private_key] -L 11111:127.0.0.1:8080 ubuntu@129.70.51.111
```

... creates a network tunnel from **A** to **B** via **C**, where 

- A is our local machine **[localhost:]1111** 
- B is Theia-IDE process bind to **127.0.0.1:8080** on our vm. 
- C is the **floating ip** of our instance, e.g. **129.70.51.111**

Start a browser, open the URL [http://localhost:11111](http://localhost:11111) and enjoy Theia-IDE.

## UserData
When providing the [theia-ide script](web-ide.sh) as userdata, we have to make some additional configuration.  We have to pay attenttion for ...

### permissions
Userdata scripts are always executed as root. We have to take care that our IDE is executable as *normal* user.
### network connectivity
The web-ide.sh script requires an existing network connection, therefore it has to wait for the network to be setup before it starts. The shell function *wait_for_service* from the UserData tutorial will help us to solve the problem.
Just wait if an external web page (e.g. Openstack Horizon) is available.
```sh
wait_for_service cloud.bi.denbi.de 443
```
### automatic system updates
Some cloud images (like Ubuntu) checks for updates when getting an internet connection. During the update check any package installation is blocked.
### service  
As you may know data/scripts provided as userdata are only considered at the very first start of a virtual machine. We have to take care that the IDE is run on every (re-)boot of our virtual machine. An relative easy way to achieve is to add an systemd startup script for our Theia-IDE service.

We have to write a wrapper script (theia-ide.sh) to start the IDE, place it in IDE install dir (`${HOME}/IDE`) and make it executable.

```sh
#!/bin/bash
source ${HOME}/.nvm/nvm.sh
cd $(dirname ${0})
yarn theia start ${HOME} --hostname 127.0.0.1 --port 8080
```

As 2nd step we have to define a systemd service `theia-ide`, place it in `/etc/systemd/system/` ... 

```sh
[Unit]
Description=Theia-IDE service for user ubuntu
After=network.target
StartLimitIntervalSec=0

[Service]
Type=simple
Restart=always
RestartSec=1
User=ubuntu
ExecStart=/home/ubuntu/IDE/theia-ide.sh 

[Install]
WantedBy=multi-user.target
```

... and enable/start it.


```sh
> systemctl enable theia-ide.service
> systemctl start theia-ide.service
```



Download a [Download](userdata.sh) userdata script that wraps up everything mentioned above.


## Ansible

Another (more flexible) way to setup Theia-IDE on a virtual machine is to write an ansible role. Fortunately there is a predefined role available on [ansible-galaxy](https://galaxy.ansible.com), that allows us to setup Theia-IDE without much effort. Browse to [https://galaxy.ansible.com/jkrue/theia_ide](https://galaxy.ansible.com/jkrue/theia_ide) and follow the ReadMe.


