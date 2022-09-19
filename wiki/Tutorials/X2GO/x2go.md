# X2Go 

!!! Deprecated
    We offer to install [Apache Guacamole](../../simple_vm/customization.md#apache-guacamole) on your virtual machines with a single click while starting up. It allows you to use the user interface of your machine at any time without an additional client via your favourite web browser - no further configuration on your part is necessary. 

X2Go allows you to start your own desktop in the de.NBI Cloud which you can access from any operating system (Windows, Linux, MacOS).

## Installation

#### First Steps

In order to install X2Go, connect to the corresponding machine first.
Make sure, that the `software-properties-common` package is installed. On Ubuntu 16.04 and higher the package should already have the newest version. 

Run the following commands to install the X2Go-server on your machine.
> sudo add-apt-repository ppa:x2go/stable

> sudo apt-get update

> sudo apt-get install x2goserver x2goserver-xsession

In the next step, install a desktop binding for the desktop environment you like.
In this tutorial we will use `LXDE`, but you can find bindings and install instructions for several environments [here](https://wiki.x2go.org/doku.php/wiki:advanced:desktopbindings).

For LXDE, run the following commands:
> sudo apt install aptitude

> sudo aptitude install x2golxdebindings

#### Export key in OpenSSH format for X2GO (Windows only)
To connect to a machine with X2GO you have to export your private key in openssh format. To achieve this first load your private key into puttygen.

![X2Go Client](../../portal/img/putty_private.png)

Then click Conversions and choose Export OpenSSH Key. Afterwards save this file on your computer. This file will be needed when you want to establish a connection to a machine with the X2GO client.

![SSH_export](../../portal/img/putty_export.png)

## Usage

#### Connect to X2GO machine

To connect to X2Go, you need a client e.g the X2Go client you can find [here](https://wiki.x2go.org/doku.php/download:start).
As a macOS user make sure that [XQuartz](https://www.xquartz.org) is installed.

When you start the X2Go client, you need to enter the session preferences first.
Choose any name you like for the session.
The following data, most of which can be found on the details page of the VM running X2Go, is of relevance:
- The IP of the machine
- The port of the machine
- The path of your private key. The key can be easily selected via the user interface
- The username for the connection to the machine. By default this is `ubuntu`

![X2Go Information](../../portal/img/x2go_session.png)


Select your private key, which you use to connect to the machine.
For the session type select `LXDE` or any other desktop environment you have installed in advance.
The IP is the first marked information on the previous picture. The port is the second marked information. 
This information can be found as described on the details page of your VM.

After you have saved the session preferences, you can now select the session and connect to the machine.

![X2Go Client](../../portal/img/x2go_client.png)




