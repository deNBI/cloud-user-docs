#SSH keys and sharing access


##Basic
You need to set up a ssh key pair in your Profile. This key is needed so you can access the virtual machine via ssh. You should
under no circumstances share your private key with someone.


##Sharing Access
If you want to share access to one of your virtual machines the person you want to share it to needs to give you their public ssh key.
If they do not have a ssh key pair yet, they need to generate it, e.g., using ssh-keygen. After you have obtained their public key you need to
add the key to your virtual machine.

If you are using a Linux distribution this can be done via the following command:

> ssh-copy-id -i {PUBLIC_KEY} -p {PORT} ubuntu@{IP_ADDRESS}

You can find the PORT and the IP_ADDRESS in you virtual machine overview under "Connect Information". PUBLIC_KEY is the name and path of
the public ssh key of the person that you want to share access to.

Otherwise, use the following steps to add a user to a virtual machine

1.
Connect to your machine as usual.

2.
Use the command:
> nano .ssh/authorized_keys

This opens the file in which all your keys are saved who have access to your virtual machine. Your key is already in that file, do not change it.

3.
Copy the public key of the person you want to add (important- not the private key) and add it to the line after your key to the file.
Using CTRL-X you can close the file. When you are closing the file you are asked whether you want to save your changes. Please confirm this.

Now the other user can access your virtual machine. If you run into troubles please contact us via cloud-portal-support@deNBI.de.

##Reminder
Please only add the ssh key of people you trust. Furthermore, you are still responsible for the virtual machine if you share your
access with other people.
