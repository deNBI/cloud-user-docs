### MTU fix for docker

In case you use docker containers in your VM it may happen that the building 
process of the containers will fail or you can not download packages. The reason is that docker can not connect to the 
internet. The problem is caused by different mtu values for the host and the 
docker container. To fix the problem you have to add the correct mtu value to 
the following file:

     /lib/systemd/system/docker.service

Add **--mtu=1440** to the end of the **ExecStart** line in the [Service] 
section, like shown below:

    ExecStart=/usr/bin/docker daemon -H fd:// --mtu=1440
    
In a last step you have to reload the daemon and restart docker:

    sudo systemctl daemon-reload
    sudo systemctl docker restart

Now the docker build process should be successful.
