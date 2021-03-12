# Enable concurrent sessions for Guacamole 

Per default, the Guacamole research environment allows for one concurrent session per username on the machine. Therefore 
multiple persons can not be logged in with the same username.  
To have multiple persons logged in with different usernames, you will need to add them first by following these steps.  

## Add user to research environment
If you have not done so already add the user to your research environment in the 
[instance detail page](./instance_detail.md#user-management) under "User management".

![user_management](./img/instance_detail/user_management.png)  

## Add new user to the machine
### With guacamole
Access Guacamole as usual using the link provided in "How to connect" of your virtual machine in the instance overview
or detail page.

#### Open the terminal
Open a new terminal window (see image).  
![guacamole_terminal](./img/guacamole/guacamole_terminal.png)  

#### Create a new user

Add a new user using the following command:
```bash
$ sudo adduser USERNAME
```

Instead of USERNAME use the actual name that you want to use. It can be chosen arbitrarily.
It is important that you remember the password when it is asked. The other questions can be
left blank (just use enter to skip). A new home directory will be created for USERNAME.

#### Grant root privileges (optional)
If you want to give the new user root (admin) privileges use the following command:

```bash
$ sudo usermod -aG sudo USERNAME
```

Fill in the actual name for USERNAME.

#### Install gedit (optional)
If you are unfamiliar with the editors nano or vi it makes sense to install gedit as 
it is easier to use. In order to install gedit, use the following command:

```bash
$ sudo apt-get install gedit
```

#### Add user to Guacamole
Now you need to add the new user to Guacamole. If you installed gedit use it to open this file:

```bash
$ sudo gedit /etc/guacamole/user-mapping.xml
```

Otherwise, use the editor of your choice, e.g. vi:

```bash
$ sudo vi /etc/guacamole/user-mapping.xml
```

Add the following lines to the file (in between the tags `<user-mapping>`, but after the tag `</authorize>`, see image):

![file_position](./img/guacamole/file_position.png)  

```xml
        <authorize
                username="USERNAME-FOR-WEB-LOGIN"
                password="PASSWORD-FOR-WEB-LOGIN">

        <connection name="Ubuntu Server">
                <protocol>rdp</protocol>
                <param name="hostname">127.0.0.1</param>
                <param name="port">3389</param>
                <param name="username">USERNAME-YOU-CREATED</param>
                <param name="password">PASSWORD-YOU-CREATED</param>
        </connection>

        </authorize>
```

Here you will need to fill the following four variables.  
`USERNAME-FOR-WEB-LOGIN` and `PASSWORD-FOR-WEB-LOGIN` will be the credentials the user will log in with when 
using the web browser. The can be the same as the credentials you used when creating the user but they also can be 
different.  
`USERNAME-YOU-CREATED` and `PASSWORD-YOU-CREATED` are the username and password you chose when creating the new user.  

Save and close the file (use STRG + s in order to save, if you are using gedit).

###  Finish
Now another user can log in with the credentials `USERNAME-FOR-WEB-LOGIN` and `PASSWORD-FOR-WEB-LOGIN` to start a concurrent 
session while you are running your main session using the default credentials. Please note that you need to repeat this 
process (with different usernames) for every user which wants to run a concurrent Guacamole session on this virtual machine.
