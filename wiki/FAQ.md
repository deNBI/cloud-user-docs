## General

### How much do I have to pay for a de.NBI Cloud project? Who can use the cloud?

You don't have to pay for a de.NBI Cloud project! It is free for all academic life science research projects.
Each project running in the de.NBI Cloud requires a Principal Investigator of a German university or research
institution as project owner.

### The site of my project requires a login name ? Where do I find it?

Some compute center sites use a JumpHost to connect to your machines.
There, a username must sometimes be entered for authentication.
Please check this in the site-specific wiki section.

The user name is not expected to be your Elixir ID, but your LifeScience login.
You can find it on your [profile page](portal/user_information.md) in the portal.

Please also note: In the past, authentication - also for the portal - was done via Elixir AAI.
Recently, authentication was transferred to LifeScience AAI. The Elixir ID remains your unique identifier within the
Virtual Organisation, but is distinct from the LifeScience login.

### I cannot access my virtual machine?

At first try to restart the machine.
If this does not bring the desired success, the reasons can be manifold.

Make sure that you use the correct SSH key!
If you have changed your SSH key in the portal since creating the machine, it will not be automatically changed on this
machine. The connection to this VM still requires the key that was set at the time of creation. The private key is
always used to connect to the machine.

You can find more about SSH keys [here]({{extra.simplevm_wiki_link}}simple_vm/keypairs/).

Maintenance may be performed at the site where your machines are running. Occasionally, malfunctions also occur during
regular service.
Check your project site's [Facility News](https://cloud.denbi.de/news/facility-news/) page - downtimes are usually
announced on this page.
In addition, we have a [status page](https://status.cloud.denbi.de/status/default) where you can check the respective
services.

### What are flavors? Which flavor should I choose for my VM?

Flavor determine the hardware resources available for their virtual machine. During the process of starting the VM, you
will see the flavors that are available to you.
Applications or more complex pipelines that require high memory or compute should be run on flavors with more VCPUs
and/or RAM. For certain use cases from the fields of artificial intelligence or data mining, GPU flavors can be useful.
This is also true if CUDA is part of your pipeline.

### The resources available to my project are not sufficient. How can I apply for more resources?

As an administrator of your project, you can submit
a [modification request](./portal/modification.md#resource-modifications) in
the [project overview](./portal/project_overview.md).

### My project is about to expire. Can I extend it? What happens to my virtual machines?

Project [extension requests](./portal/modification.md#lifetime-extensions) can also be submitted in the project
overview.
When the project expires, your virtual machines are not automatically deleted. Before any steps of this kind are taken,
a member of the cloud administration will contact you in any case.

### I am confused about what project type suits best?

If the information on the Project Type Overview page is not sufficient, more information on project types is available
on our [website](https://cloud.denbi.de/about/project-types/). This information is also linked on the Project Type
Overview page.

Maintenance may be performed at the site where your machines are running. Occasionally, malfunctions also occur during
regular service.
Check your project site's [Facility News](https://cloud.denbi.de/news/facility-news/) page - downtimes are usually
announced on this page.
In addition, we have a [status page](https://status.cloud.denbi.de/status/default) where you can check the respective
services.

### Where can I find the support contact details?

Check our [support](https://cloud.denbi.de/support/) page, it lists the email addresses of the facilities.

### Are there any testimonials about working with the de.NBI Cloud?

Yes, take a look [here](https://cloud.denbi.de/about/testimonials/)!

### How can I acknowledge the de.NBI Cloud in publications?

See [here](../citation_and_publication/#citation-information) for more information.

### Where can I find the terms of use and privacy policy?

Take a look [here](https://cloud.denbi.de/about/policies/).

## SimpleVM

### My VM is stuck in "build" or "checking connection" status? What does this mean?

An error may have occurred while creating the machine. If the machine is not available even after a longer period of
time, feel free to contact us so that we can take a look at the situation.

### My machine is marked as "NOT FOUND". What does this imply?

The machine may no longer exist in OpenStack. If you have any questions regarding your virtual machine, please feel free
to contact us.

## Miscellaneous

### I can not build docker images and can not download packages from inside of the container.

In case you use docker containers in your VM it may happen that the building
process of the containers will fail or you can not download packages. The reason is that docker can not connect to the
internet. The problem is caused by different mtu values for the host and the
docker container. To fix the problem you have to add the correct mtu value to
the following file:

     /lib/systemd/system/docker.service

Add **--mtu=1440** to the end of the **ExecStart** line in the [Service]
section, like shown below:

    ExecStart=/usr/bin/docker daemon -H fd:// --mtu=1440

Or you can add this to **/etc/docker/daemon.json**

    {
          "mtu": 1440
    }    

In a last step you have to reload the daemon and restart docker:

    sudo systemctl daemon-reload
    sudo systemctl restart docker

Now the docker build process should be successful.

