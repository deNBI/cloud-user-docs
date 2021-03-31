# Enable concurrent sessions for RStudio

Per default, the RStudio research environment allows for one concurrent session per username on the machine. Therefore 
multiple persons can not be logged in with the same username.  
To have multiple persons logged in with different usernames, you will need to add them first by following these steps.  

## Add user to research environment
If you have not done so already add the user to your research environment in the 
[instance detail page](./instance_detail.md#user-management) under "User management".

![user_management](./img/instance_detail/user_management.png)  

## Add new user to the machine
### With RStudio
Access RStudio as usual using the link provided in "How to connect" of your virtual machine in the instance overview
or detail page.

#### Open the terminal
Open the terminal tab (see image).  
![rstudio_terminal](./img/rstudio/rstudio_terminal.png)  

#### Create a new user

Add a new user using the following command:
```bash
$ sudo adduser USERNAME
```

Instead of USERNAME use the actual name that you want to use. It can be chosen arbitrarily.
It is important that you remember the password when it is asked. The other questions can be
left blank (just use enter to skip). A new home directory will be created for USERNAME.

![rstudio_add_user](./img/rstudio/rstudio_add_user.png)

!!! danger "Warning"
    Due to the nature of the research environment, the password you choose is not hidden when typing it, as you may see
    in the picture above.

#### Grant root privileges (optional)
If you want to give the new user root (admin) privileges use the following command:

```bash
$ sudo usermod -aG sudo USERNAME
```

Fill in the actual name for USERNAME.

###  Finish
Now another user can log in with the credentials `USERNAME` and `PASSWORD` you created earlier to start a concurrent 
session while you are running your main session using the default credentials. Please note that you need to repeat this 
process (with different usernames) for every user which wants to run a concurrent RStudio session on this virtual machine.
