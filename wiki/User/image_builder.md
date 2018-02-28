# Diskimage Builder

## Installing Diskimage Builder

[ Github diskimage-builder repo](https://github.com/openstack/diskimage-builder)

[ Openstack diskimage-builder user install guide](http://docs.openstack.org/developer/diskimage-builder/user_guide/installation.html )

First, update your system as **root**:

	
	$ apt-get update 
	$ apt-get upgrade


To install the **diskimage-builder** on your instance, you need pip. Run as **root**

	
	$ apt-get install python-pip


After this, install the **diskimage-builder** with pip as **root**:

	
	$ pip install diskimage-builder
	$ apt-get install qemu-utils


### Errors while installing

#### Language Package

Depending on your locale settings or installed language-packages, it can happen that this error occur:

	Traceback (most recent call last):
	    File "/usr/bin/pip", line 11, in `<module>`
	    sys.exit(main())
	    File "/usr/lib/python2.7/dist-packages/pip/__init__.py", line 215, in main
	    locale.setlocale(locale.LC_ALL, '')
    	    File "/usr/lib/python2.7/locale.py", line 581, in setlocale
    	    return _setlocale(category, locale)
	    locale.Error: unsupported locale setting

This can be resolved by installing your language-pack. For german, run as **root**

	
	$ apt-get install language-pack-de

Check your 2 letters country code [here](http://www.worldatlas.com/aatlas/ctycodes.htm)

#### Unresolved Hostname

To prevent an error like this:

        sudo: unable to resolve host `<name_of_instance>`



in /etc/hosts, add the name of the instance as **root**

        127.0.0.1 localhost `<name_of_instance>`

The following lines are desirable for IPv6 capable hosts

        ::1 ip6-localhost ip6-loopback
        fe00::0 ip6-localnet
        ff00::0 ip6-mcastprefix
        ff02::1 ip6-allnodes
        ff02::2 ip6-allrouters
        ff02::3 ip6-allhosts

## Create a new Disk Image

Basically, invoking the following command is sufficient to create a new image:

	
	$ disk-image-create ubuntu vm 


Images can be customized by specifying further arguments. Read the following sections to learn more about customizing your image.


*  -a architecture

*  -o target output file

*  -p package name[s]

*  elements

### Elements

Nevertheless, images can be customized either by passing package identifiers or element names.
Corresponding the OpenStack documentation, elements define "what goes into [the] image and what modifications will be performed". For an bootable image, one should at least provide two Elements, **vm** which "[s]ets up a partitioned disk (rather than building just one filesystem with no partition table)" and a **distribution name** (e.g. Ubuntu, CentOS, OpenSUSE). Whereas we recommend Ubuntu, due to the entire documentation covers Ubuntu examples.

See [ here](https://github.com/openstack/diskimage-builder/tree/master/elements ) for a list of pre-built elements.

Adding more elements to the image during the creation process can simply achieved be append them to the end of the function call:

	$ disk-image-create ubuntu vm docker # Note: Element 'docker' needs further parameters


An element defines steps for each phase of the creation cycle. Every single step could be implemented as a Bash or Python script. Have a look [ here]( http://docs.openstack.org/developer/diskimage-builder/developer/developing_elements.html#phase-subdirectories ) to learn more about the single stages.

###  Packages

As mentioned above, packages which are available through the, e.g. Ubuntu, [ package repository ]( http://packages.ubuntu.com/ ), could be installed during the creation process by simply append package names.

	# create Ubuntu Trusty as qcow2 image
	$ disk-image-create -a amd64 -o ubuntu-trusty.qcow ubuntu vm
	
	# create Ubuntu Trusty as qcow2 image, additionally install Tomcat from Ubuntu repositories
	$ disk-image-create -a amd64 -o ubuntu-trusty-with-tomcat.qcow -p tomcat8 ubuntu vm
	
	# create Ubuntu 16.04 (Xenial) as qcow2 image and Tomcat
	$ DIB_RELEASE=xenial disk-image-create -a amd64 -o ubuntu-xenial-with-tomcat.qcow -p tomcat8 ubuntu vm
	


### Create own Elements 

Developing new elements is straightforward. All one have to do is to create an executable script containing the command and place it within a directory of the right execution stage (see section Elements). 

For example, placing the following script in ''/path/to/elements/clojure-boot/install.d'' instructs the image builder to create an image with Boot, a build tool for the Clojure programming language, pre-installed:

```bash
#!/bin/bash

set -eu
set -o pipefail

sudo bash -c "cd /usr/local/bin && \ 
              curl -fsSLo boot https://github.com/boot-clj/boot-bin/releases/download/latest/boot.sh && \ 
              chmod 755 boot"

```

Don't forget to set right permissions:

```bash
chmod +x 01-clojure-boot
```

Additionally, pointing the environment variable ''ELEMENTS_PATH'' to a custom directory, let you define a personal element path:

```bash
export ELEMENTS_PATH=/home/ubuntu/elements/
```

By default, all elements are located in ''/usr/local/share/diskimage-builder/elements''. Have a look [ here]( http://docs.openstack.org/developer/diskimage-builder/elements.html ) or [ here ]( https://github.com/openstack/diskimage-builder/tree/master/elements ) to examine whether a desired element already exists or which elements are available, in general.

**Note:** All executable files without extension are executed, thus removing the executable flag prevents the image builder to execute those files.

In order to create your customized image, simply invoke:

```bash
# creates image with GNU Octave, Octave documentation and gnuplot (from Ubuntu repository)
# identifier of the custom element have to match with directory name (/path/to/elements/clojure-boot)
disk-image-create -a amd64 -o ubuntu-with-clojure.qcow2 -p octave,octave-doc,gnuplot ubuntu vm clojure-boot
```

#### Docker install latest

This is an example for using shell scripts to install packages manually
https://get.docker.com/

```bash	
mkdir -p elements/latest_docker/install.d
cd elements/latest_docker/install.d
```

Edit file ''10-latest-docker'' in ''install.d''. Pay attention that you don't use file extensions. Additionally, you have to use a [shebang](https://en.wikipedia.org/wiki/Shebang_(Unix)).

```bash
#!/bin/bash

curl https://get.docker.com | sh
```

```bash	
chmod a+x 10-latest-docker
disk-image-create -a amd64 -o ubuntu-trusty_dap.qcow2 ubuntu vm latest_docker
```

### package-installs.yaml

Placing a ''package-installs.yaml'' into a element directory is further way to specify packages, which should be installed.

Basically, the yaml file has the following structure:


```yaml
---
package:version
```

See [ here ]( http://docs.openstack.org/developer/diskimage-builder/elements/package-installs/README.html ) for more details.

#### Example Docker

To remember the path of the host home directory:

```bash
home=$(dirname $0)
```

You need a system variable ''ELEMENTS_PATH'' with the path to your elements:

```bash	
mkdir /home/ubuntu/elements
export ELEMENTS_PATH=/home/ubuntu/elements/

mkdir -p /home/ubuntu/elements/docker_as_package && cd /home/ubuntu/elements/docker_as_package
touch package-installs.yaml
```

Edit package-installs.yaml

```yaml
---
docker.io:
```

Finally, create your new image by invoking the following command:

```bash
$ disk-image-create -a amd64 -o ubuntu-trusty_dap.qcow2 ubuntu vm docker_as_package
```

## Upload Image (via CLI)

As soon your image was successfully created, it's possible to upload and register the image in Glance, the OpenStack service to manage images, via the command line.

Firstly, one have to set up neccessary user credentials to "set[...] variables in your shell that allow you to interact with OpenStack services". For this purpose, enter the "Access & Security" screen and switch to the "API Access" tab. Here, download the ''OpenStack RC File V3''. 

Afterwards, issue the following commands:

```bash	
source `<name of your project>`-openrc.sh
sudo apt-get install python-openstackclient
openstack
(openstack) router list
(openstack) help
```

The command below will upload your image. After the upload is completed, an image called ''dlatest'' should be available through the "Images" tab, within the OpenStack dashboard.


*  --disk-format qcow2

*  --file `<path_to_file>`

*  `<image-name >`

##### Example 1

```	
(openstack) image create --disk-format qcow2 --file ubuntu-trusty_dlatest.qcow2 dlatest
```

##### Example 2

```
(openstack) image create --disk-format qcow2 --file /home/ubuntu/ubuntu-trusty_dap.qcow2 docker_as_a_package
```

