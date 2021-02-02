## Security aspects of cloud computing

### Shift in responsibility

One important change triggered by the rise of cloud computing is a shift in responsibility.
In the pre-cloud world, a system administrator was responsible for taking care of the system,
installing security patches and fixes, securing the network, setting up firewalls and monitoring
the operation state of servers.

With cloud computing, this has changed considerably:
The system administrator is still responsible for the bare
hardware servers. However, the user-created instances (virtual machines) running on these servers
are the sole responsibility of the user who launched them. This includes any activity going on
inside the instances while they are running as well as all of their
communication with the outside world.

Large compute ressources and unrestricted high-speed internet access make cloud instances
an attractive target for outside attackers. Users are obligated to keep their instances
secure and up-to-date.

### General security recommendations

- SSH access: Always use key based authentication instead of a plain password.

- Keep the operating system and all installed packages of your instances up to date.

- Make sure to always use the most recent of the officially provided cloud images when
  launching a new instance.

- Configure the internal firewall of your instances using `iptables` to add another layer of
  security in addition to the security groups.

- Do not rely on any global cloud site firewall, its configuration might change without
  prior notice. If in doubt, ask the site administrators!

If you have detected a possible security problem with an instance, please contact the site
administrators immediately and ask for support. They will to advise you on how to proceed.

### Best practices for remote port access

#### SSH port forwarding

SSH is able to forward a port through a tunnel and make it available to your local computer only.
No security group rule needed! So e.g. to access a server listening on port `localhost:8080` of your
instance, you forward it to `127.0.0.1:8080` on your local computer by adding the following to your
SSH call: `-L 127.0.0.1:8080:localhost:8080`. A server serving a website would then be available at
`http://127.0.0.1:8080`.

Further information:

- [http://help.ubuntu.com/community/SSH/OpenSSH/PortForwarding](http://help.ubuntu.com/community/SSH/OpenSSH/PortForwarding)

#### Well defined remote IP range

Allow access from only a subset of IP addresses, e.g. from the Bielefeld University IP range:
`129.70.0.0/16` (That is only about 0.002% of the world's IPv4 addresses). The default security
group (which all new instances get) should not be touched. Create a new one instead, add your rules
and attach it only to the instance you need outside access to.

Further information:

- [https://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing#CIDR_notation](https://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing#CIDR_notation)

#### Application security

Many applications support authentication (e.g. username and password). Use it to stop any outside
attacks that were (easily) able to guess your instance's IP and port (which are not secret by any
means). It is also highly recommended to protect your network traffic from prying eyes using TLS
which is available inside almost all server applications, especially webservers.

**Always** change the default credentials of services as these are well known and
will be probed as soon as the service is exposed to the internet.
