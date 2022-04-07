# Persistent Terminal Sessions
When you connect to your vm via ssh a session is created. <br>
A problem with this is that all programs you start during this session will also be terminated when you close your SSH connection.
<br><br>To work around this problem there are ways to create persistent sessions.<br>
In this short tutorial this is shown with **screen**.

## Screen - Terminal Multiplexer
Screen is a terminal multiplexer that allows you to create sessions in which any number of windows can be opened.
The important feature is that these sessions are persistent and independent of the SSH session.

### 1. Install screen on your vm
```bash

$ sudo apt update
$ sudo apt install screen
```

### 1. Start a (named) screen session
```bash

$ screen -S session_name
```

### 2. You can list all screen sessions
```bash
$ screen -ls

There is a screen on:
        616541.session_name     (23.03.2022 13:40:15)   (Attached)


```
Currently "session_name" is the only available session.

### 3. These sessions are persistent until you delete them - even if you disconnect and reconnect via ssh
### 4. You can always create new sessions and attach and detach them
```bash
$ screen -ls

There are screens on:
        616612.session_two      (23.03.2022 13:40:22)   (Attached)
        616541.session_name     (23.03.2022 13:40:15)   (Detached)
```
Pressing: <kbd>Ctrl</kbd> + <kbd>A</kbd>,  <kbd>d</kbd> (detaching Session)

```bash
$ screen -ls

There are screens on:
        616612.session_two      (23.03.2022 13:40:22)   (Detached)
        616541.session_name     (23.03.2022 13:40:15)   (Detached)

```
Attach a Session via id:
```bash
$ screen -r 616541
$ screen -ls
There are screens on:
        616612.session_two      (23.03.2022 13:40:22)   (Detached)
        616541.session_name     (23.03.2022 13:40:15)   (Attached)

```

This way you can easily create persistent sessions with screen that are independent of the ssh session.<br> Screen also offers other useful features such as the creation of several windows.

## Useful Links/Commands:

- Screen Cheatsheet - https://quickref.me/screen


- Manpage: [Screen](https://linux.die.net/man/1/screen) or
```bash 
$ man screen

```

- Good alternative: [TMUX](https://tmuxguide.readthedocs.io/en/latest/tmux/tmux.html)