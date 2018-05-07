## Security aspects in clouds

One important change triggered by the rise of clouds is a shift in responsibility. In the pre-cloud world, a system administrator was responsible for taking care of system, installing security patches and fixes, securing the network, settings up firewalls and monitor the operation state of servers.

With clouds, this has changed. The system administrator is still responsible for the servers, but is focusing on the cloud setup itself. An inspection of running instances is technically difficult (if not infeasible), and in case of extern users' instance legally forbidden. Monitoring is restricted to transfer points like network interfaces, and may allow the administrator to detect abuse or suspicious actions.

As a result, the user or group starting and managing their instances are responsible for them. It's up to them to ensure that the systems are updated in a properly manner, and set up in a secure way to prevent abuse or instances being compromised.

This page hosts a list of recommendations every cloud user should follow. This list is neither complete nor comprehensive, and will be extended over time:

*  Do not use password based logins, always use SSH with key only

*  Keep the operation system and installed packages in each instance up to date, especially in long running ones

*  Update images to contain the latest patches (and ask the site administrators to update images provided by them)

*  Use security groups and a white list of allowed ports to control access to your instances

*  Restrict access even further if possible, e.g. by restricting to certain IP networks

*  **ALWAYS** change the default credentials of services, these credentials are well known and will be probed if the service is exposed to the internet

*  Configure the firewall of the instance in addition to the security groups, every additional layer will help

*  Do not rely on a cloud site firewall, its configuration might change without prior notice. If in doubt, ask the site administrators!

If you have detected a possible security problem with an instance, contact the site administrator and ask for support. He/she should be able to advise you how to proceed.
