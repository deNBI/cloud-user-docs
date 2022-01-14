### How much do I have to pay for a de.NBI Cloud project?

The de.NBI Cloud is fully funded by the federal ministry of education and research. It is free for all academic life science research projects.

### I cannot access my virtual machine?

Make sure that you use the correct SSH key!
If you have changed your SSH key in the portal since creating the machine, it will not be automatically changed on this machine. The connection to this VM still requires the key that was set at the time of creation. The private key is always used to connect to the machine.
You can find more about SSH keys [here](./simple_vm/keypairs/#ssh-keys-and-sharing-access).

### How can I acknowledge the de.NBI Cloud in publications?

See [here](../citation_and_publication/#citation-information) for more information.

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

